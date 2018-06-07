'''
Created on 2018/04/25
last edit 2018/5/22
@author: kim
GUI based ipfw controler
check bridge773
if not, won't run
###ToDo
File input output
implement function about pipe or bridge later


ExEnvKaerutyan ver.0.1.0

'''
import cv2
import time
import sys
import netifaces
import threading
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import date, datetime as dt
from PyQt5.QtGui import QFont,QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.Qt import QPalette
import subprocess
from symbol import except_clause
import random

class EnvChanger(QMainWindow):
    def __init__(self, parent=None,initials=None):
        QWidget.__init__(self)
        # variables
        self.font = QFont('Serif', 22, QFont.Light)
        self.ret_flg = False

        self.env_num = -1
        self.delay_num = -1
        self.plr_num = -1

        # Menu Bar
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addMenu("Save")
        self.file_menu.addMenu("Open")

        # status bar
        self.statusBar()
        self.statusBar().showMessage("Experiment Environment Changer")

        #env num
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(20, 30, 200, 30)
        self.lbl_fname.setFont(QFont("Serif", 18, QFont.Light))
        self.lbl_fname.setText("Env:")
        self.qle_id = QLineEdit(self)
        self.qle_id.setGeometry(90, 30, 70, 30)
        self.qle_id.setFont(QFont("Serif", 16, QFont.Light))
        self.qle_id.textChanged[str].connect(self.on_env_text_input)

        #delay
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(20, 80, 200, 30)
        self.lbl_fname.setFont(QFont("Serif", 18, QFont.Light))
        self.lbl_fname.setText("Delay:")
        self.qle_id = QLineEdit(self)
        self.qle_id.setGeometry(90, 80, 70, 30)
        self.qle_id.setFont(QFont("Serif", 16, QFont.Light))
        self.qle_id.textChanged[str].connect(self.on_delay_text_input)
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(165, 85, 240, 30)
        self.lbl_fname.setFont(QFont("Serif", 14, QFont.Light))
        self.lbl_fname.setText("ms")

        #plr
        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(20, 130, 200, 30)
        self.lbl_fname.setFont(QFont("Serif", 18, QFont.Light))
        self.lbl_fname.setText("plr:")
        self.qle_id = QLineEdit(self)
        self.qle_id.setGeometry(90, 130, 70, 30)
        self.qle_id.setFont(QFont("Serif", 16, QFont.Light))
        self.qle_id.textChanged[str].connect(self.on_plr_text_input)

        self.lbl_fname = QLabel(self)
        self.lbl_fname.setGeometry(165, 135, 240, 30)
        self.lbl_fname.setFont(QFont("Serif", 14, QFont.Light))
        self.lbl_fname.setText("%")

        self.add_button = self.put_add_button()
        self.apply_button = self.put_apply_button()
        self.delete_button = self.put_delete_button()
        self.randomize_button = self.put_randomize_button()

        self.env_list_table = QTableWidget(self)
        self.env_list_table.setGeometry(240,25,230,210)
        self.env_list_table.setColumnCount(1)
        self.env_list_table.setColumnWidth(0,231)
        self.env_list_table.setRowHeight(100,15)
        self.row_num = 0

        self.env_list = {}

        item1 = QtWidgets.QTableWidgetItem('Environments')
        item1.setBackground(QtGui.QColor(0, 255, 127))
        self.env_list_table.setHorizontalHeaderItem(0,item1)

        self.env_list_table.verticalHeader().hide()
        self.env_list_table.verticalHeader().setDefaultSectionSize(20)
        self.env_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # size and title
        self.setGeometry(220, 220, 490, 300)
        self.setWindowTitle("")
        self.show()

    def put_add_button(self):
        btn = QPushButton("add", self)
        btn.setFont(QFont('Serif', 18, QFont.Light))
        btn.setStyleSheet("color : blue")
        btn.setGeometry(8, 185, 70, 35)
        btn.setEnabled(True)
        btn.clicked.connect(self.button_event_add)
        return btn

    def button_event_add(self):
        if self.env_num >= 0 and self.delay_num >= 0 and self.plr_num >= 0:
            self.env_list[int(self.env_num)] = "delay "+str(self.delay_num)+"ms plr "+str(self.plr_num)

            print(self.env_list[self.env_num])
            self.env_list_table.setRowCount(len(self.env_list))
            i = 0
            for k,v in sorted(self.env_list.items(), key = lambda x:x[0]):
                self.env_list_table.setItem(0, i, QTableWidgetItem(str(k)+".  " + str(v)))
                print(str(v))
                i = i + 1


    def put_apply_button(self):
        btn = QPushButton("apply", self)
        btn.setFont(QFont('Serif', 18, QFont.Light))
        btn.setStyleSheet("color : green")
        btn.setGeometry(85, 185, 70, 35)
        btn.setEnabled(True)
        btn.clicked.connect(self.button_event_apply)
        return btn

    def button_event_apply(self):
        try:
            if len(self.env_list_table.selectedItems())>0:
                cmd = self.env_list_table.selectedItems()[0].text().split("  ")
                if len(cmd) < 2:
                    raise Exception("cmd error")
                print("ipfw pipe 773 config "+ cmd[1])
                subprocess.check_call("ipfw pipe 773 config "+ cmd[1])
                self.statusBar().showMessage("setting " + cmd[0])
                self.env_list_table.selectedItems()[0].setBackgraund

            else :
                print("please select environment")

        except Exception as e:
            self.statusBar().showMessage("failed to call ipfw")
            sub = SubWindow(self)
            sub.show()

        finally:
            self.env_list_table.clearSelection()

    def put_delete_button(self):
        btn = QPushButton("delete", self)
        btn.setFont(QFont('Serif', 18, QFont.Light))
        btn.setStyleSheet("color : red")
        btn.setGeometry(163, 185, 70, 35)
        btn.setEnabled(True)
        btn.clicked.connect(self.button_event_delete)
        return btn

    def button_event_delete(self):
        try:
            if len(self.env_list_table.selectedItems())>0:
                cmd = self.env_list_table.selectedItems()[0].text().split("  ")
                if len(cmd) < 2:
                    raise Exception("fatal error")
                index = int(cmd[0].replace(".",""))
                del self.env_list[index]
                self.env_list_table.setRowCount(len(self.env_list))
                i = 0
                for k,v in sorted(self.env_list.items(), key = lambda x:x[0]):
                    self.env_list_table.setItem(0, i, QTableWidgetItem(str(k)+".  " + str(v)))
                    print(str(v))
                    i = i + 1
                self.env_list_table.clearSelection()
            else :
                print("please select environment")

        except Exception as e:
            print(e.message)
            qApp.quit()

    def put_randomize_button(self):
        btn = QPushButton("randomaize", self)
        btn.setFont(QFont('Serif', 14, QFont.Light))
        btn.setGeometry(370, 240, 100, 25)
        btn.setEnabled(True)
        btn.clicked.connect(self.button_event_randomize)
        return btn

    def button_event_randomize(self):
        print()
        i = 0
        for k in random.sample(list(self.env_list.keys()),len(self.env_list)):
            self.env_list_table.setItem(0, i, QTableWidgetItem(str(k)+".  " + str(self.env_list[k])))
            i = i + 1

    def on_env_text_input(self,text):
        if text.isnumeric():
            self.env_num = int(text)
        else :
            self.statusBar().showMessage("Invalid input:Env")
            self.env_num = -1

    def on_delay_text_input(self,text):
        if text.isnumeric():
            self.delay_num = int(text)
        else :
            self.statusBar().showMessage("Invalid input:delay")
            self.delay_num = -1

    def on_plr_text_input(self,text):
        if text.isnumeric():
            self.plr_num = int(text)/100
        else :
            self.statusBar().showMessage("Invalid input:plr")
            self.plr_num = -1


class SubWindow:
    def __init__(self, parent=None):
        self.w = QDialog(parent)
        self.parent = parent
        self.font = QFont('Serif', 22, QFont.Light)

        label = QLabel()
        label.setText('ipfw excution FAILED')
        label.setFont(self.font)
        label.setStyleSheet("color: red")
        btn = QPushButton('Exit')
        btn.clicked.connect(self.w.close)
        btn.setFont(QFont("Serif", 14, QFont.Light))
        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn)
        main_layout.addLayout(btn_layout)

        self.w.setLayout(main_layout)

        self.w.setGeometry(320, 320, 280, 160)

    def show(self):
        self.w.exec_()


def create_main_window(argv):
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion')) # won't work on windows style.
    EC = EnvChanger()
    EC.show()
    try:
        app.exec_()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    print("This is Experiment Environment Changer ver.0.0.1. \n[NOTICE]Thre are many un impremented functions and unknown bugs \nConfigure gridge773 and pipe773 mannualy\n\n")
    if u'bridge773' in netifaces.interfaces() or True:
        create_main_window(sys.argv)
#     elif subprocess.call("ifconfig bridge773 create".split("" )):
    else:
        print("Im sorry Im not so credible so please configure network interfaces and ipfw command.")