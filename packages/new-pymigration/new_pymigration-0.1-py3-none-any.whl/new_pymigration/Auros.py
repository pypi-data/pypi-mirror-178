# -*- coding: utf-8 -*-
"""
Created on 2022 년 9월 7일

made by HN Park
"""

import sqlite3
import pyodbc
import pandas as pd
from PyQt5.QtCore import *
import cleasing as cs
import pandas.io.sql as psql
from pandas import ExcelWriter


onecall = cs.open_info()
query_list = onecall[0].copy()
field_names = onecall[1].copy()
cnt_question = onecall[2].copy()
only_cols = onecall[3].copy()
eq_dic = onecall[4].copy()

pyload_df = {}

def sqlite_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = sqlite3.connect(db_file)
    return conn

def pyodbc_create_connection(ip):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + ip + ';DATABASE=AurosDB;UID=sa;PWD=nano*2008')
    return conn

def Get_IPAddress(ip):
    conn = pyodbc_create_connection(ip)
    cur = conn.cursor()
    cur.execute(f"SELECT EquipmentID, Name  FROM EquipmentConfigurations")

    row = cur.fetchall()
    return row

def equipment_info(ip, name):
    conn = pyodbc_create_connection(ip)
    cur = conn.cursor()
    cur.execute(f"SELECT EquipmentID FROM EquipmentConfigurations WHERE Name = '{name}'")
    row = [item[0] for item in cur.fetchall()]
    return row


def pyodbc_select(cur, col, table, value, state):
    if state == 1:
        sql = f"SELECT * FROM dbo.{table}"

    if state == 2:
        sql = f"SELECT {col} FROM dbo.{table}"

    if state == 3:
        sql = f"SELECT {col} FROM dbo.{table} WHERE {value[0]} between '{value[1]} 00:00:00.000' and '{value[2]} 00:00:00.000'"

    cur.execute(sql)


def pyodbc_insert(cur, col, table, value, state):

    if state == 1:
        sql = f"INSERT INTO {table} ({col}) VALUES ({cnt_question[value[0]]})"

    if state == 2:
        cur.fast_executemany = True
        sql = f"INSERT INTO {table} ({col}) VALUES ({cnt_question[value[0]]})"

    cur.executemany(sql, value[1])

def get_dataframe(path, k, v, curs):
    df = pd.read_excel(path, sheet_name=k)
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    df = df.fillna(0)
    matching_id = [s for s in v if "ID" in s]

    if matching_id:
        pyodbc_select(curs, f'{matching_id[0]}', f'{k}_new', None, 2)
        row = [item[0] for item in curs.fetchall()]
        res_df = df[~df[f'{matching_id[0]}'].isin(row)]
    else:
        res_df = df

    return res_df

class get_sql_to_db(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.log.append("[Start sql_to_db]...")
        try:
            for index, (k, v) in enumerate(eq_dic.items()):

                self.parent.log.append("[Processing sql_to_db]_Connecting...")
                path = self.parent.path[0].replace('.db',f'_{k}.db')
                conn = pyodbc_create_connection(v)
                sl3Conn = sqlite_connection(f'{path}')
                c = sl3Conn.cursor()
                cur = conn.cursor()

                for index, (k, v) in enumerate(query_list.items()):
                    self.parent.log.append("[Processing sql_to_db]_Getting...")
                    col = ', '.join(only_cols[index])
                    cnt_idx = list(cnt_question.keys())[index]

                    c.execute(f'CREATE TABLE IF NOT EXISTS {k} ({field_names[k]})')

                    matching = [s for s in v if "Time" in s]
                    if matching:
                        pyodbc_select(cur, col, k, [matching[0],self.parent.STime,self.parent.ETime], 3)
                    else:
                        pyodbc_select(cur, col, k, None, 2)
                    rows = cur.fetchall()

                    pyodbc_insert(c, col, k, [cnt_idx, rows], 1)
                sl3Conn.commit()
                self.parent.log.append("[Done sql_to_db]!!")

        except sqlite3.Error as error:
            sl3Conn.commit()
            self.parent.log.append("Failed to read data from table", error)
        finally:
            if sl3Conn:
                sl3Conn.close()
                print("The Sqlite connection is closed")
        self.quit()
        self.wait(3000)

class get_db_to_csv(QThread):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.log.append("[Start db_to_csv]...")
        try:
            for file in self.parent.path[0]:
                name = file.split('/')[-1]
                self.parent.log.append(f"[Processing db_to_csv]_Connecting '{name}'...")
                conn = sqlite3.connect(f'{file}')

                df = {}
                writer = ExcelWriter(f"S{self.parent.STime}_E{self.parent.ETime}_from '{name}'.xlsx")
                for index, (k, v) in enumerate(query_list.items()):
                    self.parent.log.append(f"[Processing db_to_csv]_Getting '{k}'...")
                    sql = f'SELECT * FROM {k}'
                    df[k] = psql.read_sql(sql, conn)
                    df[k].to_excel(writer, k)
                self.parent.log.append(f"[Processing db_to_csv]_Saving Data from '{name}'...")
                writer.save()
                conn.close()

            self.parent.log.append("[Done db_to_csv]!!")

        except:
            self.parent.log.append("Failed to save the data, Max of Excel size is 1048576 Please check the data amount.")

        self.quit()
        self.wait(3000)

class get_csv_to_aurosdb(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.log.append("[Start csv_to_aurosdb]...")

        try:
            for index, (k, v) in enumerate(eq_dic.items()):
                self.parent.log.append(f"[Processing csv_to_aurosdb]_Connecting '{k}'...")
                conn = pyodbc_create_connection(v)
                curs = conn.cursor()

                for file in self.parent.path[0]:
                    if k in file: #file 이름과 FAB ID가 같은것을 찾음
                        self.parent.log.append(f"[Processing csv_to_aurosdb]_Preparing '{k}'...")
                        for index, (k, v) in enumerate(query_list.items()):
                            col = ', '.join(only_cols[index])
                            cnt_idx = list(cnt_question.keys())[index]

                            matching_id = [s for s in v if "ID" in s]

                            #없앨거임
                            try:
                                curs.execute(f'CREATE TABLE dbo.{k}_new ({field_names[k]} CONSTRAINT PK_{k}_new PRIMARY KEY ({matching_id[0]}) )')
                            except:
                                pass

                            try:
                                df = get_dataframe(file, k, v, curs)
                                rows = df.values.tolist()
                                self.parent.log.append(f"[Processing csv_to_aurosdb]_Setting '{k}'..")
                                pyodbc_insert(curs, col, f'{k}_new', [cnt_idx, rows], 2)
                            except:
                                self.parent.log.append(f"Already exist '{k}'.. OR There is No Data")
                                pass

                            conn.commit()
            self.parent.log.append("[Done csv_to_aurosdb]!!")

        except pyodbc.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()
                print("The Sqlite connection is closed")

        self.quit()
        self.wait(3000)

class get_pyload(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.log.append("[Start load csv to py]...")

        path = self.parent.path[0]
        df = {}
        for index, (k, v) in enumerate(query_list.items()):
            # root = [s for s in file if k in s][0]
            self.parent.log.append(f"[Processing load csv to py]...{k}")
            df[k] = pd.read_excel(path, sheet_name=k)
            df[k].drop(df[k].columns[df[k].columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
            df[k] = df[k].fillna(0)

        pyload_df[path] = df
        self.parent.log.append("[Done load csv to py]!!")

