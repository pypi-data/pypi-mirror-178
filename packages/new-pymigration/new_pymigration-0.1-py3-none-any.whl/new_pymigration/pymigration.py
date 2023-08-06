# -*- coding: utf-8 -*-
"""
Created on 2022 년 9월 7일

made by HN Park
"""

import sys
from PyQt5.QtWidgets import *
import pyConverterUI as CUI

if __name__ == '__main__':

    app = QApplication(sys.argv)
    hnpark = CUI.MainWindow()
    hnpark.show()
    app.exec_()

