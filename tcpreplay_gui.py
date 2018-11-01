# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:36:40 2018

@author: fd
"""

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 18:00:59 2018

@author: key1234
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 14:24:35 2018

@author: fd
"""

import sys
import time
import subprocess
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QApplication, QPushButton, QInputDialog,
                             QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QTabWidget, QSlider, QCheckBox,
                             QMessageBox, QScrollArea,QTextBrowser)

config_dic = {}
send_list = {}
res_cmd = ""
tab_name = []
pcap_path = "./pcap/"
twolineflag = 0


class Checkboxlist(QtWidgets.QWidget):
    def __init__(self, test_type):
        self.test_type = test_type
        if test_type not in send_list.keys():
            send_list[test_type] = []
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        items = config_dic[test_type]
        for txt in items.keys():
            id_ = items[txt]
            checkBox = QtWidgets.QCheckBox(txt, self)
            checkBox.id_ = id_
            checkBox.stateChanged.connect(self.checkLanguage)
            layout.addWidget(checkBox)

        self.lMessage = QtWidgets.QLabel(self)
        layout.addWidget(self.lMessage)
        self.setLayout(layout)

    def checkLanguage(self, state):
        checkBox = self.sender()
        if state == QtCore.Qt.Unchecked:
            for _ in checkBox.id_:
                send_list[self.test_type].remove(_)
        elif state == QtCore.Qt.Checked:
            for _ in checkBox.id_:
                send_list[self.test_type].append(_)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def connect(self):
        if self.IPbox.text() == "":
            text, ok = QInputDialog.getText(self, 'Input Dialog', '输入IP:')
            if ok:
                self.IPbox.setText(str(text))
#        if self.usernamebox.text() == "":
#            text, ok = QInputDialog.getText(self, 'Input Dialog', '输入用户名:')
#            if ok:
#                self.usernamebox.setText(str(text))
#        if self.passwordbox.text() == "":
#            text, ok = QInputDialog.getText(self, 'Input Dialog', '输入密码:')
#            if ok:
#                self.passwordbox.setText(str(text))
#        if self.ethbox.text() == "":
#            text, ok = QInputDialog.getText(self, 'Input Dialog', '输入网口号:(eg:eth1)')
#            if ok:
#                self.ethbox.setText(str(text))
        self.IP = self.IPbox.text()
        self.username = self.usernamebox.text()
        self.password = self.passwordbox.text()
        self.eth = self.ethbox.text()
        QMessageBox.information(self, "", "需要一段时间，请等待")
        #a, b = subprocess.getstatusoutput('ping ' + self.IP)  # a是退出状态 b是输出的结果
        self.thread_connect= MyThread(re='ping  -t 100 -c 2 ' + self.IP)  # 创建一个线程 发送cmd
        self.thread_connect.sec_changed_signal.connect(self.update_state_connect)  # cmd线程发过来的信号挂接到槽：update_state
        #self.thread2.sec_changed_signal.connect(self.update_time)  # 计时线程发过来的信号挂接到槽：update_time       
        self.thread_connect.start()
    def  update_state_connect(self,b):
        self.resultbox.setText(b)
        if "ms" in b and "100% packet loss" not in b:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "注意",
                                    "连接成功")
        else:
            QMessageBox.information(self, "注意", "连接失败 请检查IP设置")
        self.thread_connect.terminate()
       

    def update(self):
        QApplication.processEvents()

    def read_json(self):
        global config_dic
        global res_cmd
        global send_list
        global tab_name
        global pcap_path
        global twolineflag

        try:
            fname = QFileDialog.getOpenFileName(self,
                                                "选取文件",
                                                "./",  # 起始路径
                                                "配置文件 (*.json)")  # 设置文件扩展名过滤,用双分号间隔

            with open(fname[0], 'r') as load_f:
                config_dic = json.load(load_f)
                send_list = {}
                res_cmd = ""
                tab_name = []
                pcap_path = ""
                res_cmd = fname[0]
                self.tab.clear()
                for test_type in config_dic.keys():
                    send_list[test_type] = []
                    tab_name.append(test_type)
                    self.tab.test_type = Checkboxlist(test_type)
                    l = int(len(test_type) / 2)
                    s = test_type[0:l] + '\n' * twolineflag + test_type[l:]
                    self.tab.addTab(self.tab.test_type, s)
                self.update()
        except:
            return 1

    def initUI(self):
        # 读取配置文件
        global config_dic
        global twolineflag
        try:
            with open('config.json', 'r') as load_f:
                config_dic = json.load(load_f)
        except:
            config_dic = config_dic
            QMessageBox.information(self,  # 使用infomation信息框
                                    "注意",
                                    "未找到配置文件 请手动选择")
            self.read_json()
            # 初始化连接
        self.IPbox = QLineEdit()
        #self.IPbox.setText("192.168.201.129")
        self.re_num = 1
        self.usernamebox = QLineEdit()
        self.ethbox = QLineEdit()
        self.passwordbox = QLineEdit()
        self.connect_button = QPushButton("测试连接")
        self.update_button = QPushButton("更新配置")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("被测试IP:"))
        hbox1.addWidget(self.IPbox)
        hbox1.addWidget(self.connect_button)
        hbox1.addWidget(QLabel("      "))
        hbox1.addWidget(QLabel("本机用户名:"))
        hbox1.addWidget(self.usernamebox)
        hbox1.addWidget(QLabel("本机密码:"))
        hbox1.addWidget(self.passwordbox)
        hbox1.addWidget(QLabel("网口号:"))
        hbox1.addWidget(self.ethbox)

        hbox1.addWidget(self.update_button)

        self.connect_button.clicked.connect(self.connect)
        self.update_button.clicked.connect(self.read_json)

        # 中间

        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(2500, 2000)  #######设置滚动条的尺寸
        self.tab = QTabWidget()
        for test_type in config_dic.keys():
            send_list[test_type] = []
            tab_name.append(test_type)

            self.tab.test_type = Checkboxlist(test_type)
            l = int(len(test_type) / 2)
            s = test_type[0:l] + '\n' * twolineflag + test_type[l:]
            self.tab.addTab(self.tab.test_type, s)
        # tab.tabBar().setFixedHeight(48)
        hbox2 = QHBoxLayout(self.topFiller)
        hbox2.addWidget(self.tab)
        #hbox2.addWidget(self.scroll)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)


        # 辅助功能
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        self.re_timebox = QSlider(Qt.Horizontal, self)
        self.re_timebox.setMinimum(1)
        self.re_timebox.setMaximum(1000)
        self.re_timebox.valueChanged[int].connect(self.changeValue)
        self.num = QLabel("1")
        self.fullspeed = QCheckBox("全速发送")
        hbox3.addWidget(self.fullspeed)  # -R

        hbox4.addWidget(QLabel("  重复次数:"))
        hbox4.addWidget(self.num)
        hbox4.addWidget(self.re_timebox)

        hbox3.addWidget(QLabel("  最大发包数量:"))
        self.maxpacknumbox = QLineEdit()  # -L
        hbox3.addWidget(self.maxpacknumbox)
        hbox3.addWidget(QLabel("  每秒发送报文数:"))
        self.packpsbox = QLineEdit()  # -p
        hbox3.addWidget(self.packpsbox)

        '''hbox3.addWidget(QLabel("  指定MTU:"))
        self.MTUbox = QLineEdit()  # -t
        hbox3.addWidget(self.MTUbox)'''

        hbox3.addWidget(QLabel("发包速度/Mbps:"))
        self.Mbpsbox = QLineEdit()
        hbox3.addWidget(self.Mbpsbox)

        # 开始测试
        self.start_button = QPushButton("开始发送数据包")
        self.start_button.clicked.connect(self.start_test)
        self.stop_button = QPushButton("停止发送数据包")
        self.stop_button.clicked.connect(self.stop_test)
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.start_button)
        hbox5.addWidget(self.stop_button)
        #        hbox5.addWidget(QLabel("                            time："))
        #        self.timebox = QLineEdit()
        #        hbox5.addWidget(self.timebox)
        # 显示输出结果
        self.resultbox = QTextBrowser()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(QLabel("选择测试模式："))

        #vbox.addLayout(hbox2)
        vbox.addWidget(self.scroll)
        vbox.addWidget(QLabel("可选项："))
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        vbox.addLayout(hbox5)
        vbox.addWidget(QLabel("状态提示信息："))
        vbox.addWidget(self.resultbox)
        self.setLayout(vbox)
        # self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('tcpreplay_gui')
        self.show()

    def changeValue(self, value):
        self.num.setText(str(value))
        self.re_num = value

    def stop_test(self):
        if "数据包发送成功"  not in self.resultbox.toPlainText() and " 默认发包速度下" in self.resultbox.toPlainText() :
            try:
                self.thread.terminate()
                self.thread2.terminate()
                self.resultbox.setText("")
            except:
                self.resultbox.setText("")
        else:
            self.resultbox.setText("")
            

    def start_test(self):
        self.resultbox.setText("")

        # tcprewrite是否需要
        self.resultbox.setText("")
        # -i 设置eth端口
        if self.ethbox.text() == "":
            text, ok = QInputDialog.getText(self, 'Input Dialog', '输入网口号:(eg:eth1)')
            if ok:
                self.ethbox.setText(str(text))
        if self.passwordbox.text() == "":
            text, ok = QInputDialog.getText(self, 'Input Dialog', '输入密码')
            if ok:
                self.passwordbox.setText(str(text))
        re = "echo " + self.passwordbox.text() + "|sudo -S " + "tcpreplay -i " + self.ethbox.text() + " "
        # 最大速率发送 -t
        if self.fullspeed.isChecked():
            re += " -t "
        else:
            re = re
        # 重复次数
        if self.re_num > 1:
            re = re + "-l " + str(self.re_num) + " "
        ''''#制定MTU
        if not self.MTUbox.text()=="":
            re+=" - "+ self.MTUbox.text()+' '''''

        # 每秒发包数量
        if not self.packpsbox.text() == "":
            re += ' -p ' + self.packpsbox.text() + ' '
        # 发送速度MB/s
        if not self.Mbpsbox.text() == "":
            re += ' -M ' + self.Mbpsbox.text() + ' '
        # 最大发包数量
        if not self.maxpacknumbox.text() == "":
            re += ' -L ' + self.maxpacknumbox.text() + ' '
        # 数据包名称 路径应和json文件位置相同
        tabindex = self.tab.currentIndex()
        tn = (tab_name[tabindex])
        pcaplist = send_list[tn]
        if len(pcaplist) == 0:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "注意",
                                    "请选择至少一个包")
            return
        if len(pcaplist) == 1:
            re +=pcap_path+pcaplist[0]
        else:
            temp = re
            re = ""
            for i in pcaplist:
                re += temp + pcap_path+i + " &&"
            re = re[0:-2]

       # self.resultbox.setText(self.resultbox.toPlainText() + '\r\n' + re)
        self.starttime = time.time()
        self.resultbox.setText(self.resultbox.toPlainText() + '\r\n' + "正在发送数据包 默认发包速度下可能需要较长时间 请耐心等待。。。")
        self.thread = MyThread(re=re)  # 创建一个线程 发送cmd
        self.thread2 = MyThread2(self.starttime)  # 创建一个线程 计时

        self.thread.sec_changed_signal.connect(self.update_state)  # cmd线程发过来的信号挂接到槽：update_state
        self.thread2.sec_changed_signal.connect(self.update_time)  # 计时线程发过来的信号挂接到槽：update_time
        self.thread.start()
        self.thread2.start()

    def update_state(self, b):
        if "Actual" in b:
            self.resultbox.setText("数据包发送成功！" + '\r\n结果统计信息：\r\n' + b[b.index("Actual"):])
        else:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "注意",
                                    "未能成功发送 请检查网口设置与软件是否正确安装")

        # self.resultbox.setText(self.resultbox.toPlainText() + '\r\n' + b)
        self.thread.terminate()
        self.thread2.terminate()

    def update_time(self, a):
        self.resultbox.setText(
            self.resultbox.toPlainText() + '\r\n' + "已用时间：" + str(round(time.time() - self.starttime)) + "s")


class MyThread(QThread):
    sec_changed_signal = pyqtSignal(str)  # 信号类型：int

    def __init__(self, re=None, parent=None):
        super().__init__(parent)
        self.re = re

    def run(self):
        a, b = subprocess.getstatusoutput(self.re)
        self.sec_changed_signal.emit(b)  # 发射信号


class MyThread2(QThread):
    sec_changed_signal = pyqtSignal(str)

    def __init__(self, re=None, parent=None):
        super().__init__(parent)
        self.re = re
        self.isrunning = True

    def run(self):
        b = " "
        for i in range(1000):
            time.sleep(5)
            self.sec_changed_signal.emit(b)  # 发射信号

    def stop(self):
        self.isrunning = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
