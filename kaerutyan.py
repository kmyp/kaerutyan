'''
Created on 2018/04/25

@author: kim
'''
import cv2
import time
import sys
import threading
import os
from datetime import date, datetime as dt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont,QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import *
from PyQt5.Qt import QPalette
from PyQt5.uic.Compiler.qtproxies import QtCore, QtWidgets

class EnvChanger(QtWidgets.QFrame):
    def __init__(self, parent=None,initials=None):
        QtWidgets.QFrame.__init__(self)
        # variables
        self.font = QFont('Serif', 22, QFont.Light)
        self.ret_flg = False

        # status bar
        self.statusBar()
        self.statusBar().showMessage("Experiment Environment Changer")

        #env num
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(20, 20, 200, 30)
        self.lbl_fname.setFont(QFont("Serif", 18, QFont.Light))
        self.lbl_fname.setText("Env:")
        self.qle_id = QLineEdit(self)
        self.qle_id.setGeometry(90, 20, 70, 30)
        self.qle_id.setFont(QFont("Serif", 16, QFont.Light))
        self.qle_id.textChanged[str].connect(self.on_env_text_input)

        #delay
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(20, 70, 200, 30)
        self.lbl_fname.setFont(QFont("Serif", 18, QFont.Light))
        self.lbl_fname.setText("Delay:")
        self.qle_id = QLineEdit(self)
        self.qle_id.setGeometry(90, 70, 70, 30)
        self.qle_id.setFont(QFont("Serif", 16, QFont.Light))
        self.qle_id.textChanged[str].connect(self.on_env_text_input)
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(165, 75, 240, 30)
        self.lbl_fname.setFont(QFont("Serif", 14, QFont.Light))
        self.lbl_fname.setText("ms")

        #plr
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(20, 120, 200, 30)
        self.lbl_fname.setFont(QFont("Serif", 18, QFont.Light))
        self.lbl_fname.setText("plr:")
        self.qle_id = QLineEdit(self)
        self.qle_id.setGeometry(90, 120, 70, 30)
        self.qle_id.setFont(QFont("Serif", 16, QFont.Light))
        self.qle_id.textChanged[str].connect(self.on_env_text_input)

        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(165, 125, 240, 30)
        self.lbl_fname.setFont(QFont("Serif", 14, QFont.Light))
        self.lbl_fname.setText("%")

        self.add_button = self.put_add_button()
        self.apply_button = self.put_apply_button()




        self.env_list_table = QTableWidget(self)
        self.env_list_table.setGeometry(240,10,230,210)
        self.env_list_table.setColumnCount(1)
        self.env_list_table.setColumnWidth(0,231)
        self.env_list_table.setRowCount(4)
        self.env_list_table.setRowHeight(100,15)

        self.env_list_table.setItem(0,0, QTableWidgetItem("Tom"))
        self.env_list_table.setItem(1,0, QTableWidgetItem("Ken"))
        self.env_list_table.setItem(2,0, QTableWidgetItem("Susie"))
        self.env_list_table.setItem(3,0, QTableWidgetItem("Kevin"))

        #remove header

        item1 = QtWidgets.QTableWidgetItem('red')
        item1.setBackground(QtGui.QColor(255, 0, 0))
        self.env_list_table.setHorizontalHeaderItem(0,item1)

        self.env_list_table.verticalHeader().hide()
        self.env_list_table.verticalHeader().setDefaultSectionSize(20)
        self.env_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)





        # size and title
        self.setGeometry(220, 220, 490, 280)
        self.setWindowTitle("")
        self.show()

    def put_add_button(self):
        btn = QPushButton("add", self)
        btn.setFont(QFont('Serif', 18, QFont.Light))
        btn.setStyleSheet("color : blue")
        btn.setGeometry(30, 175, 70, 35)
        btn.setEnabled(True)
        btn.clicked.connect(self.button_event_add)
        return btn

    def button_event_add(self):
        print("hello")


    def put_apply_button(self):
        btn = QPushButton("apply", self)
        btn.setFont(QFont('Serif', 18, QFont.Light))
        btn.setStyleSheet("color : red")
        btn.setGeometry(110, 175, 70, 35)
        btn.setEnabled(True)
        btn.clicked.connect(self.button_event_apply)
        return btn

    def button_event_apply(self):
        print("hello")


    def on_env_text_input(self):
        print("hello")



def create_main_window(argv):
    app = QApplication(argv)
    EC = EnvChanger()
    sys.exit(app.exec_())

if __name__ == "__main__":
    create_main_window(sys.argv)