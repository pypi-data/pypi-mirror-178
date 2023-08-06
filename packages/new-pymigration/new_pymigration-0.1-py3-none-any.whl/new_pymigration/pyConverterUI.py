# -*- coding: utf-8 -*-
"""
Created on 2022 년 9월 7일

made by HN Park
"""

# UI 제작
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import time
import pandas as pd
import cleasing as cs
import Auros
import datetime
import csv


def set_machine(path):
    for j in path:
        for i in list(Auros.eq_dic.keys()):
            if i in j:
                return i
            else:
                pass


class CldDate(QDialog):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Date Search')
        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)
        layout = QVBoxLayout()
        layout.addWidget(self.cal)
        self.setLayout(layout)


####################################################################################################
################           First Main Viewer that shows a recipe list        ########################
####################################################################################################

eqip_values = []
class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.Get_IP()
        self.mainsetupUI()

    def Get_IP(self):
        iplist = {}
        for index, (k, v) in enumerate(Auros.eq_dic.items()):
            iplist[v] = Auros.Get_IPAddress(v)

        for index, (k,v) in enumerate(iplist.items()):
            for j in range(len(v)):
                eqip_values.append(v[j][1])
        print(f'equipmentID: {eqip_values}')

    def mainsetupUI(self):
        self.setGeometry(200, 50, 800, 700)
        self.setWindowTitle("pyMigration_v0")
        self.setWindowIcon(QIcon('icon.png'))

        self.LblMachine = QLabel("FAB#", self)
        self.LblEQIP = QLabel("EQ IP#", self)
        self.LblTbl = QLabel("Tables")
        self.LblSrtDate = QLabel("Data Range Start", self)
        self.LblEndDate = QLabel("Data Range End", self)

        self.cmbMachine = QComboBox(self)
        self.cmbEQIP = QComboBox(self)
        self.cmbTbl = QComboBox(self)
        self.SrtDate = QCheckBox("Date", self)
        self.EndDate = QCheckBox("Date", self)

        self.SrtDate.stateChanged.connect(self.Srt_Action)
        self.EndDate.stateChanged.connect(self.End_Action)

        self.SrtDate.setText((datetime.datetime.now() - datetime.timedelta(days=40)).strftime("%Y-%m-%d"))
        self.EndDate.setText((datetime.datetime.now() - datetime.timedelta(days=35)).strftime("%Y-%m-%d"))

        self.SrtcldDate = CldDate()
        self.EndcldDate = CldDate()

        self.log = QTextEdit()
        self.log.setFixedHeight(70)

        self.tblSearch1 = QTableWidget(self)
        self.tblSearch1.setColumnCount(50)
        self.tblSearch1.setRowCount(50)
        self.tblSearch1.horizontalHeader().setStretchLastSection(True)
        self.tblSearch1.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.SQlitebtn = QPushButton("save file", self)
        self.csvbtn = QPushButton("cvt file", self)
        self.pyloadbtn = QPushButton("load file", self)
        self.toAurDBtbtn = QPushButton("into AurosDB", self)
        self.Applybtn =  QPushButton("apply", self)
        self.Reportbtn = QPushButton("report", self)

        self.SQlitebtn.clicked.connect(self.sql_to_db)
        self.csvbtn.clicked.connect(self.db_to_csv)
        self.pyloadbtn.clicked.connect(self.pyload_connection)
        self.Applybtn.clicked.connect(self.apply_condition)
        self.toAurDBtbtn.clicked.connect(self.db_to_aurosdb)
        self.Reportbtn.clicked.connect(lambda state, widget=self.tblSearch1: self.report_result( widget))

        condi_layout = QHBoxLayout()
        condi_layout.addWidget(self.LblMachine)
        condi_layout.addWidget(self.cmbMachine)
        condi_layout.addWidget(self.LblEQIP)
        condi_layout.addWidget(self.cmbEQIP)
        condi_layout.addWidget(self.LblTbl)
        condi_layout.addWidget(self.cmbTbl)

        Layout1 = QFormLayout()
        Layout1.addRow(condi_layout)
        Layout1.addRow(self.LblSrtDate, self.SrtDate)
        Layout1.addRow(self.LblEndDate, self.EndDate)
        Layout1.addRow(self.tblSearch1)

        Layout2 = QHBoxLayout()
        Layout2.addWidget(self.SQlitebtn)
        Layout2.addWidget(self.csvbtn)
        Layout2.addWidget(self.pyloadbtn)
        Layout2.addWidget(self.Applybtn)
        Layout2.addWidget(self.Reportbtn)
        Layout2.addWidget(self.toAurDBtbtn)

        Connectwg = QVBoxLayout()
        Connectwg.addLayout(Layout1)
        Connectwg.addLayout(Layout2)
        Connectwg.addWidget(self.log)

        self.setLayout(Connectwg)

        self.toAurDBtbtn.setEnabled(True)
        self.Reportbtn.setEnabled(False)
        self.Applybtn.setEnabled(False)

        self.setting()


    def Srt_Action(self, state):
        if state == Qt.Checked:
            self.SrtDate.setEnabled(True)
            self.toggle = True

            self.SrtcldDate.show()
            self.doubleclicked = 'False'
            self.SrtcldDate.cal.clicked[QDate].connect(self.srt_showDate)
        else:
            self.toggle = False
            self.SrtDate.setText("")
            self.SrtDate.setEnabled(True)

    def srt_showDate(self, date):
        self.SrtDate.setText(date.toString("yyyy-MM-dd"))
        # self.Search_by_date()     #해당 date의 data만 불러옴
        self.SrtcldDate.close()

    def End_Action(self, state):
        if state == Qt.Checked:
            self.EndDate.setEnabled(True)

            self.EndcldDate.show()
            self.doubleclicked = 'False'
            self.EndcldDate.cal.clicked[QDate].connect(self.end_showDate)

        else:
            self.EndDate.setText("")
            self.EndDate.setEnabled(True)

    def end_showDate(self, date):
        self.EndDate.setText(date.toString("yyyy-MM-dd"))
        self.EndcldDate.close()

    ####################################################################################################
    ################       Connecting DB and Getting Data through pushbutton    ########################
    ####################################################################################################

    def sql_to_db(self):
        try:
            self.path = QFileDialog.getSaveFileName(self, "Save A File",
                                                   str('[') + str(time.strftime("%d-%b-%Y")) + str(']') + '_Save DBfile',
                                                   "DB file (*.db)")

            self.STime = self.SrtDate.text()
            self.ETime = self.EndDate.text()

            work1 = Auros.get_sql_to_db(self)
            work1.start()
        except:
            pass

    def db_to_csv(self):
        try:
            self.path = QFileDialog.getOpenFileNames(self)

            self.STime = self.SrtDate.text()
            self.ETime = self.EndDate.text()

            work2 = Auros.get_db_to_csv(self)
            work2.start()
            self.SQlitebtn.setDisabled(False)

        except:
            pass

    def db_to_aurosdb(self): #into aurosDB
        self.path = QFileDialog.getOpenFileNames(self)

        work3 = Auros.get_csv_to_aurosdb(self)
        work3.start()

    def pyload_connection(self):

        self.path = QFileDialog.getOpenFileName(self, "Excel Files (*.xls*)")
        self.cmbMachine.setCurrentText(self.path[0])

        self.ip = set_machine(self.path)
        self.cmbMachine.setCurrentText(self.ip)
        self.cmbMachine.setEnabled(False)

        try:
            work4 = Auros.get_pyload(self)
            work4.start()

            self.Applybtn.setEnabled(True)
        except:
            pass

    def apply_condition(self):#apply

        self.Reportbtn.setEnabled(True)
        self.table = str(self.cmbTbl.currentText())
        ip = self.cmbMachine.currentText()

        self.ToolID = Auros.equipment_info(Auros.eq_dic[ip], self.cmbEQIP.currentText())[0]

        STime = self.SrtDate.text()
        ETime = self.EndDate.text()

        Sdate_object = datetime.datetime.strptime(STime, "%Y-%m-%d")
        Edate_object = datetime.datetime.strptime(ETime, "%Y-%m-%d")

        try:
            df = Auros.pyload_df[self.path[0]][self.table]
            try:
                matching = [s for s in df.columns.values if "Time" in s]
                df[matching[0]] = pd.to_datetime(df[matching[0]])
                mask = (df[matching[0]] >= Sdate_object) & (df[matching[0]] <= Edate_object)
                self.filtered_df = df.loc[mask]

            except:
                self.filtered_df = df

            self.cmbchange(self.filtered_df, self.table)

        except:
            pass

    def cmbchange(self, df, table):                                        #combo 선택한 것에 따라 dataframe 생성

        tmp_df = pd.DataFrame.from_dict(df)

        if table == 'FDCLogs':
            df = tmp_df[(tmp_df['EquipmentID'] == self.ToolID)]
        else:
            df = df

        cs.dataframe_table_viewer(df, self.tblSearch1)

    def setting(self):
        m_num = Auros.eq_dic.keys()
        for idx in m_num:
            self.cmbMachine.addItem(idx)

        for idx in eqip_values:
            self.cmbEQIP.addItem(idx)

        for idx in range(len(list(Auros.field_names.keys()))):
            self.cmbTbl.addItem(str(list(Auros.field_names.keys())[idx]))


    def report_result(self, widget): #report

        self.cmbMachine = QComboBox(self)
        self.cmbEQIP = QComboBox(self)
        self.cmbTbl = QComboBox(self)

        path, ok =  QFileDialog.getSaveFileName(self, "Save A File",
                                               str(f'[') + str(time.strftime("%d-%b-%Y")) + str('] ') + 'Save Report',
                                               "Excel file (*.csv)")
        if ok:
            columns = range(widget.columnCount())
            header = [widget.horizontalHeaderItem(column).text()
                      for column in columns]
            with open(path, 'w') as csvfile:
                writer = csv.writer(
                    csvfile, dialect='excel', lineterminator='\n')
                writer.writerow(header)
                for row in range(widget.rowCount()):
                    writer.writerow(widget.item(row, column).text() for column in columns)
