import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
from pyUI import registration_ui, design, add_para, add_group, add_work, profile_ui, submit_work_ui, works_for_lesson, \
    students_for_group, see_rating, set_rating, confirm_mail
from bd.connect import *
from modules import gen_password, mail_agent, capcha
import random
import datetime
import math
import time


class Confirmpass(QtWidgets.QMainWindow, confirm_mail.Ui_MainWindow):
    def authorization(self):
        self.close()
        self.auth = Authorization()
        self.auth.show()

    def confirm_pass_fnc(self):
        input_pass = self.conf_pass_inp.text()
        current_time = datetime.datetime.now().hour  # текущее время
        less_time = (current_time - self.send_time.hour)  # прошедшее с момента отправки время(часы)
        if less_time < 5:  # если прошло меньше 5 часов
            if str(input_pass) == str(self.confirm_pass):  # если код подтверждения совпадает с отправленым кодом
                add_teacher(self.name, self.surname, self.otchestvo, self.login, self.password, self.mail)
                self.authorization()
            else:
                self.check.setText('Введён неверный код подтверждения')
        else:
            self.check.setText('Время ожидания вышло.')

    def closeEvent(self, event):
        self.authorization()

    def __init__(self, name, surname, otchestvo, login, password, mail, confirm_pass, now):
        self.name = name
        self.surname = surname
        self.otchestvo = otchestvo
        self.login = login
        self.password = password
        self.mail = mail
        self.confirm_pass = confirm_pass
        self.send_time = now
        super().__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(self.confirm_pass_fnc)


class Registration(QtWidgets.QMainWindow, registration_ui.Ui_MainWindow):
    def authorization(self):
        self.close()
        self.auth = Authorization()
        self.auth.show()

    def registration(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        otchestvo = self.otchestvo_input.text()
        login = self.login_input.text()
        password = self.password_input.text()
        password_2 = self.password_reinput.text()
        mail = self.mail_input.text()
        if login == '' or name == '' or surname == '' or otchestvo == '' or password == '' or mail == '':
            self.check.setText("Заполните все поля")
        else:
            if password == password_2:
                try:
                    check_teacher(login, password)
                    confirm_pass = random.randint(100000000000, 999999999999)
                    now = datetime.datetime.now()
                    now_time = now.isoformat()
                    mail_agent.send_mail(mail, 'ПОДТВЕРДИТЕ РЕГИСТРАЦИЮ', str(confirm_pass), now_time, name)
                    self.close()
                    self.conf_pass = Confirmpass(name, surname, otchestvo, login, password, mail, confirm_pass, now)
                    self.conf_pass.show()
                except:
                    self.check.setText("Такой пользователь уже есть")
            else:
                self.check.setText("Пароли должны совпадать")

    def show_pass(self, state):
        if state == 2:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def gen_pass(self):
        self.see_password.setChecked(True)
        self.show_pass(2)
        generated_password = gen_password.gen_password()
        self.password_input.setText(generated_password)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.registration_button.clicked.connect(self.registration)
        self.registration_button_2.clicked.connect(self.authorization)
        self.gen_pass_button.clicked.connect(self.gen_pass)
        self.see_password.stateChanged.connect(self.show_pass)


class Authorization(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def reg(self):
        self.close()
        self.reg = Registration()
        self.reg.show()

    def authorization(self):
        login = self.login_input.text()
        password = self.textEdit_2.text()
        teacher = check_teacher(login, password)

        if teacher is not None:
            file = open("auth/now.txt", "w")
            file.write(str(teacher))
            file.close()
            self.close()
            self.profile = Profile()
            self.profile.show()
        else:
            self.check.setText('Неправильный логин или пароль')
            self.auth_count += 1
            print(self.auth_count)

            if self.auth_count >= 5:
                self.login_input.setReadOnly(True)
                self.textEdit_2.setReadOnly(True)
                self.submit_capcha_button.setEnabled(True)
                self.change_capcha_button.setEnabled(True)
                self.capcha_input.setReadOnly(False)
                self.groupBox_2.show()

                self.check.setText('Введите капчу, а затем логин и пароль')
                self.change_capcha()

    def change_capcha(self):
        get_capcha = capcha.create_capcha()
        self.capcha_text = get_capcha[0]
        self.capcha.setPixmap(get_capcha[1])
        self.is_true_capcha.setText('✘')

    def inp_capcha_event(self):
        if self.capcha_input.text() == self.capcha_text:
            self.is_true_capcha.setText('✔')
            self.login_input.setReadOnly(False)
            self.textEdit_2.setReadOnly(False)
            self.submit_capcha_button.setEnabled(False)
            self.change_capcha_button.setEnabled(False)
            self.capcha_input.setReadOnly(True)
            self.check.setText('Введите логин и пароль')
        else:
            self.change_capcha()
            self.is_true_capcha.setText('✘')
            self.check.setText('Неверно введен текст с картинки')
            self.login_input.setReadOnly(True)
            self.textEdit_2.setReadOnly(True)

    def __init__(self):
        super().__init__()
        self.auth_count = 0
        self.setupUi(self)
        self.groupBox_2.hide()
        self.submit_button_2.clicked.connect(self.reg)
        self.change_capcha_button.clicked.connect(self.change_capcha)
        self.submit_button.clicked.connect(self.authorization)
        self.submit_capcha_button.clicked.connect(self.inp_capcha_event)


class Profile(QtWidgets.QMainWindow, profile_ui.Ui_MainWindow):
    def add_para(self):
        self.para = AddPara(self.rd)
        self.para.show()
        self.close()

    def add_group(self):
        self.close()
        self.group = AddGroup(self.rd)
        self.group.show()

    def add_work(self):
        self.close()
        self.work = AddWork(self.rd)
        self.work.show()

    def submit_work(self):
        self.close()
        self.submit = SubmitWork(self.rd)
        self.submit.show()

    def log_out(self):
        self.close()
        f = open("auth/now.txt", "w")
        f.close()
        self.authorization = Authorization()
        self.authorization.show()

    def show_all_labs(self):
        changed_lesson = self.listWidget.currentItem().text()
        self.wfl = WorksForLesson(self.rd, changed_lesson)
        self.wfl.show()

    def see_rating(self):
        changed_lesson = self.para_table.currentItem().text(1)
        changed_group = self.para_table.currentItem().text(0)
        changed_semester = self.para_table.currentItem().text(2)
        self.srtng = SeeRating(self.rd, changed_semester, changed_group, changed_lesson)
        self.srtng.show()

    def setRating(self):
        self.strtng = SetRating(self.rd)
        self.strtng.show()

    def std_for_gruops(self):
        changed_lesson = self.listWidget_2.currentItem().text(0)
        changed_semester = self.listWidget_2.currentItem().text(2)
        changed_group = self.listWidget_2.currentItem().text(1)
        self.sfg = StudentsForGroup(self.rd, changed_lesson, changed_group, changed_semester)
        self.sfg.show()

    def change_current_pg_num(self, value):
        if value != "":
            val = int(value)
            teacher_lessons = get_lessons(self.rd)
            self.listWidget.clear()
            current_show_count = 0
            current_lessons = []

            if self.show_with_5.isChecked():
                current_show_count = 5
            elif self.show_with_10.isChecked():
                current_show_count = 10
            elif self.show_with_15.isChecked():
                current_show_count = 15
            elif self.show_with_20.isChecked():
                current_show_count = 20

            for lesson in range(current_show_count * (val - 1),
                                current_show_count * (val - 1) + current_show_count):
                try:
                    current_lessons.append(teacher_lessons[lesson])
                except:
                    break
            self.listWidget.clear()

            for (lesson, index) in zip(current_lessons, range(0, len(current_lessons))):
                if int(index % 2) == 0:
                    i = QtWidgets.QListWidgetItem('%s' % lesson)
                    i.setBackground(QtGui.QColor('#808080'))
                    self.listWidget.addItem(i)  # Заполнение вкладки предметов
                else:
                    i = QtWidgets.QListWidgetItem('%s' % lesson)
                    i.setBackground(QtGui.QColor('#fff'))
                    self.listWidget.addItem(i)  # Заполнение вкладки предметов

    def change_next_pg_num(self):
        val = int(self.change_pg_box.currentText()) + 1
        if self.change_pg_box.count() >= val:
            index = int(self.change_pg_box.currentIndex()) + 1
            self.change_pg_box.setCurrentIndex(index)
            self.change_current_pg_num(val)

    def change_prew_pg_num(self):
        val = int(self.change_pg_box.currentText()) - 1
        if val > 0:
            index = int(self.change_pg_box.currentIndex()) - 1
            self.change_pg_box.setCurrentIndex(index)
            self.change_current_pg_num(val)

    def filing_tables(self):
        teacher_lessons = get_lessons(self.rd)
        lesson_count = len(teacher_lessons)
        current_show_count = 0
        tab_count_mas = []
        current_lessons = []

        if self.show_with_5.isChecked():
            current_show_count = 5
        elif self.show_with_10.isChecked():
            current_show_count = 10
        elif self.show_with_15.isChecked():
            current_show_count = 15
        elif self.show_with_20.isChecked():
            current_show_count = 20

        tab_count = math.ceil(lesson_count / current_show_count)

        for i in range(1, tab_count + 1):
            tab_count_mas.append(str(i))

        self.change_pg_box.clear()
        self.change_pg_box.addItems(tab_count_mas)

        for lesson in range(0, current_show_count):
            current_lessons.append(teacher_lessons[lesson])
        self.listWidget.clear()

        for (lesson, index) in zip(current_lessons, range(0, len(current_lessons))):
            if int(index % 2) == 0:
                i = QtWidgets.QListWidgetItem('%s' % lesson)
                i.setBackground(QtGui.QColor('#808080'))
                self.listWidget.addItem(i)  # Заполнение вкладки предметов
            else:
                i = QtWidgets.QListWidgetItem('%s' % lesson)
                i.setBackground(QtGui.QColor('#fff'))
                self.listWidget.addItem(i)  # Заполнение вкладки предметов

    def __init__(self, tab=0):
        super().__init__()
        # ФИО профиля
        f = open("auth/now.txt", "r")
        self.rd = f.read()
        FIO = check_teacher_for_id(self.rd)
        full_name = str(FIO[0][2]) + " " + str(FIO[0][1]) + " " + str(FIO[0][3])  # имя преподавателя
        f.close()
        _translate = QtCore.QCoreApplication.translate
        self.setupUi(self)
        self.label.setText(full_name)  # установка именя преподавателя в заголовок

        self.tabWidget.setCurrentIndex(tab)  # установка вкладки

        ololo = 0
        for i in get_teacher_groups(self.rd):
            QtWidgets.QTreeWidgetItem(self.listWidget_2)  # заполнение вкладки пары
            self.listWidget_2.topLevelItem(ololo).setText(0, str(i[0]))
            self.listWidget_2.topLevelItem(ololo).setText(2, str(i[2]))
            self.listWidget_2.topLevelItem(ololo).setText(1, str(i[1]))

            QtWidgets.QTreeWidgetItem(self.para_table)  # заполнение вкладки оценки
            self.para_table.topLevelItem(ololo).setText(0, str(i[0]))
            self.para_table.topLevelItem(ololo).setText(2, str(i[2]))
            self.para_table.topLevelItem(ololo).setText(1, str(i[1]))
            ololo += 1

        tab_count_mas = []
        current_lessons = []
        teacher_lessons = get_lessons(self.rd)
        tab_count = math.ceil(len(teacher_lessons) / 5)

        for i in range(1, tab_count + 1):
            tab_count_mas.append(str(i))
        self.change_pg_box.addItems(tab_count_mas)

        for lesson in range(0, 5):
            if int(lesson % 2) == 0:
                i = QtWidgets.QListWidgetItem('%s' % teacher_lessons[lesson])
                i.setBackground(QtGui.QColor('#808080'))
                self.listWidget.addItem(i)  # Заполнение вкладки предметов
            else:
                i = QtWidgets.QListWidgetItem('%s' % teacher_lessons[lesson])
                i.setBackground(QtGui.QColor('#fff'))
                self.listWidget.addItem(i)  # Заполнение вкладки предметов

        self.add_para_button.clicked.connect(self.add_para)
        self.add_group_button.clicked.connect(self.add_group)
        self.add_work_button.clicked.connect(self.add_work)
        self.select_submit_button.clicked.connect(self.submit_work)
        self.log_out_button.clicked.connect(self.log_out)
        self.set_rating.clicked.connect(self.setRating)
        self.listWidget.doubleClicked.connect(self.show_all_labs)
        self.para_table.doubleClicked.connect(self.see_rating)
        self.listWidget_2.doubleClicked.connect(self.std_for_gruops)
        self.show_with_5.clicked.connect(self.filing_tables)
        self.show_with_10.clicked.connect(self.filing_tables)
        self.show_with_15.clicked.connect(self.filing_tables)
        self.show_with_20.clicked.connect(self.filing_tables)
        self.change_pg_box.currentTextChanged.connect(self.change_current_pg_num)
        self.next_pg_button.clicked.connect(self.change_next_pg_num)
        self.prew_pg_button.clicked.connect(self.change_prew_pg_num)


class AddGroup(QtWidgets.QMainWindow, add_group.Ui_MainWindow):
    def add_group(self):
        if self.set_lesson.currentText() != '' and self.set_group.currentText() != '':
            id_para = get_para(self.index, get_lesson_by_text(self.set_lesson.currentText()))
            id_group = get_group_by_text(self.set_group.currentText())
            add_group_for_teacher(id_group, id_para)
            self.close()
        else:
            self.alert.setText("Заполните все поля")

    def closeEvent(self, event):
        self.profile = Profile(1)
        self.profile.show()

    def change_lesson(self):
        self.set_group.clear()
        current_id_lesson = get_lesson_by_text(self.set_lesson.currentText())
        current_id_para = get_id_para_by_teacher(self.index, current_id_lesson)
        groups = get_groups_and_paras_by_id_para(current_id_para)
        self.set_group.addItems(get_all_groups(groups))

    def back(self):
        self.close()

    def __init__(self, rd):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        print(get_lessons(self.index))
        if get_lessons(self.index):
            self.set_lesson.addItems(get_lessons(self.index))
            current_id_lesson = get_lesson_by_text(self.set_lesson.currentText())
            current_id_para = get_id_para_by_teacher(self.index, current_id_lesson)
            groups = get_groups_and_paras_by_id_para(current_id_para)
            self.set_group.addItems(get_all_groups(groups))
        self.add_button.clicked.connect(self.add_group)
        self.set_lesson.currentTextChanged.connect(self.change_lesson)
        self.back_button.clicked.connect(self.back)


class AddPara(QtWidgets.QMainWindow, add_para.Ui_MainWindow):
    def add_para_for_table(self):
        if self.para_input.currentText():
            teacher_id = self.index
            lesson_id = get_lesson_by_text(self.para_input.currentText())
            print(teacher_id, lesson_id)
            add_para_for_teacher(teacher_id, lesson_id)
            self.close()
        else:
            self.alert.setText("Предмет не выбран")

    def closeEvent(self, event):
        self.profile = Profile()
        self.profile.show()

    def back(self):
        self.close()

    def __init__(self, rd):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        self.para_input.addItems(get_all_lessons(get_lessons(self.index)))
        self.para_button.clicked.connect(self.add_para_for_table)
        self.back_button.clicked.connect(self.back)


class AddWork(QtWidgets.QMainWindow, add_work.Ui_MainWindow):
    def add_work(self):
        current_lesson_id = get_lesson_by_text(self.comboBox.currentText())
        id_para = get_para(self.index, current_lesson_id)
        work_name = self.textEdit.text()
        work_type = self.type_input.currentText()
        add_work_for_table(id_para, work_name, work_type)
        self.close()

    def closeEvent(self, event):
        self.profile = Profile()
        self.profile.show()

    def back(self):
        self.close()

    def __init__(self, rd):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        self.add_work_button.clicked.connect(self.add_work)
        self.lessons = get_lessons(self.index)
        self.comboBox.addItems(self.lessons)
        self.type_input.clear()
        self.type_input.addItems(["Лабораторная работа", "Контрольная работа"])
        self.back_button.clicked.connect(self.back)


class SeeRating(QtWidgets.QMainWindow, see_rating.Ui_MainWindow):
    def __init__(self, rd, semester='', group='', lesson=''):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        self.label_3.setText('Семестр: ' + str(semester))
        self.label_2.setText('Группа: ' + str(group))
        self.label.setText('Предмет: ' + str(lesson))
        self.current_para = get_para(self.index, get_lesson_by_text(lesson))
        ololo = 0
        for i in get_students_id_by_group(get_group_by_text(group)):
            student_and_rating = get_rating(self.current_para, i, semester)
            student = get_student_by_id(student_and_rating[0])
            rating = student_and_rating[1]
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.topLevelItem(ololo).setText(0, str(student))
            self.treeWidget.topLevelItem(ololo).setText(1, str(rating))
            ololo += 1


class SetRating(QtWidgets.QMainWindow, set_rating.Ui_MainWindow):
    def change_group(self):
        brush = QtGui.QBrush(QtGui.QColor(144, 238, 144))
        self.current_lesson = self.treeWidget.selectedItems()[0].text(1)
        self.current_semester = self.treeWidget.selectedItems()[0].text(2)
        self.current_group = self.treeWidget.selectedItems()[0].text(0)
        self.treeWidget.clear()
        item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item.setBackground(0, brush)
        item.setBackground(1, brush)
        item.setBackground(2, brush)
        self.treeWidget.topLevelItem(0).setText(0, str(self.current_group))
        self.treeWidget.topLevelItem(0).setText(1, str(self.current_lesson))
        self.treeWidget.topLevelItem(0).setText(2, str(self.current_semester))

        self.lesson_id = get_lesson_by_text(self.current_lesson)
        self.para_id = get_para(self.index, self.lesson_id)
        self.FIO_input.clear()
        self.FIO_input.addItems(
            get_students_by_group(get_group_by_text(self.current_group),
                                  get_id_graded_students(self.para_id, self.current_semester)))

    def set_change_type(self):
        if self.change_type.currentText() == 'Оценка':
            self.change_res.clear()
            self.change_res.addItems(['Неудовлетворительно', 'Удовлетворительно', 'Хорошо', 'Отлично'])
        else:
            self.change_res.clear()
            self.change_res.addItems(['Зачтено', 'Не зачтено'])

    def set_rating(self):
        fio = self.FIO_input.currentText()
        if not (self.current_lesson and self.current_semester and self.current_group) or not (fio):
            self.alert.setText('Заполните все поля!')
        else:
            name = self.FIO_input.currentText().split(" ")[0]
            surname = self.FIO_input.currentText().split(" ")[1]
            otchestvo = self.FIO_input.currentText().split(" ")[2]
            group_id = get_group_by_text(self.current_group)

            result = self.change_res.currentText()
            student_id = get_student_id(name, surname, otchestvo, group_id)
            set_rating_to_bd(student_id, self.para_id, result, self.current_semester)
            self.close()

    def back(self):
        self.close()

    def __init__(self, rd):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        self.back_button.clicked.connect(self.back)
        ololo = 0
        self.current_group = ''
        self.current_semester = ''
        self.current_lesson = ''
        for i in get_teacher_groups(self.index):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.topLevelItem(ololo).setText(0, str(i[0]))
            self.treeWidget.topLevelItem(ololo).setText(1, str(i[1]))
            self.treeWidget.topLevelItem(ololo).setText(2, str(i[2]))
            ololo += 1

        self.treeWidget.doubleClicked.connect(self.change_group)
        self.change_type.currentTextChanged.connect(self.set_change_type)
        self.pushButton.clicked.connect(self.set_rating)


class SubmitWork(QtWidgets.QMainWindow, submit_work_ui.Ui_MainWindow):
    def closeEvent(self, event):
        self.profile = Profile(1)
        self.profile.show()

    def change_group(self):
        current_lesson = self.treeWidget.selectedItems()[0].text(1)
        self.current_group = self.treeWidget.selectedItems()[0].text(0)
        self.treeWidget.clear()
        QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.topLevelItem(0).setText(0, str(self.current_group))
        self.treeWidget.topLevelItem(0).setText(1, str(current_lesson))

        id_lesson = get_lesson_by_text(current_lesson)
        self.current_id_para = get_id_para_by_teacher(self.index, id_lesson)
        works = get_works_for_para_id_1(self.current_id_para)
        ololo = 0
        for i in works:
            QtWidgets.QTreeWidgetItem(self.treeWidget_2)
            self.treeWidget_2.topLevelItem(ololo).setText(0, str(i[1]))
            self.treeWidget_2.topLevelItem(ololo).setText(1, str(i[0]))
            ololo += 1

    def change_work(self):
        current_work_name = self.treeWidget_2.selectedItems()[0].text(1)
        current_work_type = self.treeWidget_2.selectedItems()[0].text(0)
        self.treeWidget_2.clear()
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        self.treeWidget_2.topLevelItem(0).setText(0, str(current_work_type))
        self.treeWidget_2.topLevelItem(0).setText(1, str(current_work_name))
        self.current_work_id = get_id_work(self.current_id_para, current_work_name, current_work_type)
        self.FIO_input.clear()
        self.FIO_input.addItems(get_students_by_group(get_group_by_text(self.current_group),
                                                      get_students_FIO_which_submit_work(self.current_work_id)))
        print(get_students_FIO_which_submit_work(self.current_work_id))

    def submit(self):
        try:
            self.current_id_group = get_group_by_text(self.current_group)
            self.name = self.FIO_input.currentText().split(" ")[0]
            self.surname = self.FIO_input.currentText().split(" ")[1]
            self.otchestvo = self.FIO_input.currentText().split(" ")[2]
            self.current_student_id = get_student_id(self.name, self.surname, self.otchestvo, self.current_id_group)
            add_submit_work(self.current_student_id, self.current_work_id)
            self.close()
        except:
            self.alert.setText('Заполните все поля')

    def back(self):
        self.close();

    def __init__(self, rd):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        ololo = 0
        for i in get_teacher_groups(self.index):
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.topLevelItem(ololo).setText(0, str(i[0]))
            self.treeWidget.topLevelItem(ololo).setText(1, str(i[1]))
            ololo += 1

        self.treeWidget.doubleClicked.connect(self.change_group)
        self.treeWidget_2.doubleClicked.connect(self.change_work)
        self.pushButton.clicked.connect(self.submit)
        self.back_button.clicked.connect(self.back)


class WorksForLesson(QtWidgets.QMainWindow, works_for_lesson.Ui_MainWindow):
    def __init__(self, rd, changed_lesson):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        self.label.setText(changed_lesson)
        self.id_lesson = get_lesson_by_text(changed_lesson)
        self.current_id_para = get_id_para_by_teacher(self.index, self.id_lesson)
        self.works = get_works_for_para_id_1(self.current_id_para)
        ololo = 0
        for i in self.works:
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.topLevelItem(ololo).setText(0, str(i[1]))
            self.treeWidget.topLevelItem(ololo).setText(1, str(i[0]))
            ololo += 1


class StudentsForGroup(QtWidgets.QMainWindow, students_for_group.Ui_MainWindow):
    def __init__(self, rd, changed_group, changed_lesson, changed_semester):
        self.index = rd
        super().__init__()
        self.setupUi(self)
        self.label.setText('Предмет: ' + changed_lesson)
        self.label_2.setText('Группа: ' + changed_group)
        self.label_3.setText('Семестр: ' + changed_semester)
        print(changed_group)
        print(changed_lesson)
        print(changed_semester)

        self.current_id_group = get_group_by_text(changed_group)
        self.id_lesson = get_lesson_by_text(changed_lesson)
        self.current_id_para = get_id_para_by_teacher(self.index, self.id_lesson)
        self.works_id = get_works_id_for_para_id(self.current_id_para)  # Работы по паре
        for i in self.works_id:
            self.name = get_students_FIO_which_submit_work(i)
            self.surname = get_students_FIO_which_submit_work(i)
            self.otchestvo = get_students_FIO_which_submit_work(i)
            if self.name and self.surname and self.otchestvo:
                self.name = self.name[0].split(" ")[1]
                self.surname = self.surname[0].split(" ")[0]
                self.otchestvo = self.otchestvo[0].split(" ")[2]
                self.current_id_student = get_student_id(self.surname, self.name, self.otchestvo, self.current_id_group)
                if self.current_id_student is not None:
                    if check_student_in_group(self.current_id_group, self.current_id_student):
                        student = get_students_FIO_which_submit_work(i)  # студенты сдавшие работу
                        ololo = 0
                        if student:
                            for j in student:
                                item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
                                self.treeWidget.topLevelItem(ololo).setText(0, j)
                                self.treeWidget.topLevelItem(ololo).setText(1, str(get_work_by_id(i)[0]))
                                self.treeWidget.topLevelItem(ololo).setText(2, str(get_work_by_id(i)[1]))
                                ololo += 1


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    f = open("auth/now.txt", "r")
    if f.read() != "":
        prof = Profile()
        prof.show()
        app.exec()
        f.close()
    else:
        auth = Authorization()
        auth.show()
        app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
