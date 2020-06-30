# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_rating.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 650)
        MainWindow.setMinimumSize(QtCore.QSize(720, 650))
        MainWindow.setMaximumSize(QtCore.QSize(720, 650))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 590, 221, 51))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background:#121058;\n"
"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    font-family: Raleway;\n"
"    font-style: normal;\n"
"    font-weight: bold;\n"
"    font-size: 13px;\n"
"    line-height: 12px;\n"
"    color: #FFFFFF;\n"
"}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("background:#EE3327;\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"font-size:15px;\n"
"color:white;\n"
"")
        self.back_button.setObjectName("back_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 420, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("font-family: Raleway;\n"
"font-style: normal;\n"
"font-weight: bold;\n"
"font-size:15px;\n"
"")
        self.label.setObjectName("label")
        self.alert = QtWidgets.QLabel(self.centralwidget)
        self.alert.setGeometry(QtCore.QRect(150, 530, 421, 31))
        self.alert.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.alert.setStyleSheet("font-family: Raleway;\n"
"font-style: normal;\n"
"font-weight: bold;\n"
"font-size:15px;\n"
"")
        self.alert.setText("")
        self.alert.setAlignment(QtCore.Qt.AlignCenter)
        self.alert.setObjectName("alert")
        self.FIO_input = QtWidgets.QComboBox(self.centralwidget)
        self.FIO_input.setGeometry(QtCore.QRect(30, 460, 661, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.FIO_input.setFont(font)
        self.FIO_input.setStyleSheet("QComboBox {\n"
"    background:#FFF;\n"
"    border-radius: 10px;\n"
"    border:1px solid black;    \n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(C:\\/Users\\/LEMUR\\/Desktop\\/электронный помощник студента\\/ui\\/arrow.png);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 30px;\n"
"    border:0px;\n"
"}\n"
"")
        self.FIO_input.setObjectName("FIO_input")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 70, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("font-family: Raleway;\n"
"font-style: normal;\n"
"font-weight: bold;\n"
"font-size:16px;\n"
"")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(120, 330, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("font-family: Raleway;\n"
"font-style: normal;\n"
"font-weight: bold;\n"
"font-size:16px;\n"
"")
        self.label_7.setObjectName("label_7")
        self.change_type = QtWidgets.QComboBox(self.centralwidget)
        self.change_type.setGeometry(QtCore.QRect(120, 370, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.change_type.setFont(font)
        self.change_type.setMouseTracking(False)
        self.change_type.setAcceptDrops(False)
        self.change_type.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.change_type.setStyleSheet("QComboBox {\n"
"    background:#FFF;\n"
"    border-radius: 10px;\n"
"    border:1px solid black;    \n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(C:\\/Users\\/LEMUR\\/Desktop\\/электронный помощник студента\\/ui\\/arrow.png);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 30px;\n"
"    border:0px;\n"
"}\n"
"")
        self.change_type.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.change_type.setObjectName("change_type")
        self.change_type.addItem("")
        self.change_type.addItem("")
        self.change_res = QtWidgets.QComboBox(self.centralwidget)
        self.change_res.setGeometry(QtCore.QRect(410, 370, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.change_res.setFont(font)
        self.change_res.setMouseTracking(False)
        self.change_res.setAcceptDrops(False)
        self.change_res.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.change_res.setStyleSheet("QComboBox {\n"
"    background:#FFF;\n"
"    border-radius: 10px;\n"
"    border:1px solid black;    \n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(C:\\/Users\\/LEMUR\\/Desktop\\/электронный помощник студента\\/ui\\/arrow.png);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 30px;\n"
"    border:0px;\n"
"}\n"
"")
        self.change_res.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.change_res.setObjectName("change_res")
        self.change_res.addItem("")
        self.change_res.addItem("")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(410, 330, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("font-family: Raleway;\n"
"font-style: normal;\n"
"font-weight: bold;\n"
"font-size:16px;\n"
"")
        self.label_8.setObjectName("label_8")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(20, 120, 681, 192))
        self.treeWidget.setStyleSheet("background:white;\n"
"border:1px solid black;\n"
"font-size:13px;")
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setDefaultSectionSize(263)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Поставить оценку"))
        self.pushButton.setText(_translate("MainWindow", "Принять"))
        self.back_button.setText(_translate("MainWindow", "Назад"))
        self.label.setText(_translate("MainWindow", "ФИО Студента"))
        self.label_6.setText(_translate("MainWindow", "Пара"))
        self.label_7.setText(_translate("MainWindow", "Тип:"))
        self.change_type.setItemText(0, _translate("MainWindow", "Зачет"))
        self.change_type.setItemText(1, _translate("MainWindow", "Оценка"))
        self.change_res.setItemText(0, _translate("MainWindow", "Зачтено"))
        self.change_res.setItemText(1, _translate("MainWindow", "Не зачтено"))
        self.label_8.setText(_translate("MainWindow", "Результат: "))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Группа"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Предмет"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Семестр"))
