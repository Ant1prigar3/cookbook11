import random
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys
import sqlite3


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.sps = []
        self.count = 1
        self.rnd_recipe()

        self.ui.t1Button1.clicked.connect(self.nextList1)
        self.ui.t1Button2.clicked.connect(self.nextList2)
        self.ui.t1Button3.clicked.connect(self.nextList3)

        self.ui.t2Button1.clicked.connect(self.bdwork)
        self.ui.t2Button2.clicked.connect(self.backList)
        self.ui.t2Button3.clicked.connect(self.ingredien)
        self.ui.t2Button4.clicked.connect(self.openWindow1)

        self.ui.del1.hide()
        self.ui.del2.hide()
        self.ui.del3.hide()
        self.ui.del4.hide()
        self.ui.del5.hide()
        self.ui.del1.clicked.connect(self.del_ingred1)
        self.ui.del2.clicked.connect(self.del_ingred2)
        self.ui.del3.clicked.connect(self.del_ingred3)
        self.ui.del4.clicked.connect(self.del_ingred4)
        self.ui.del5.clicked.connect(self.del_ingred5)

        self.ui.t3Button1.clicked.connect(self.rnd_recipe)
        self.ui.t3Button2.clicked.connect(self.openWindow2)
        self.ui.t3Button3.clicked.connect(self.backList)

        self.ui.t4Button1.clicked.connect(self.bdinsert)
        self.ui.t4Button2.clicked.connect(self.backList)

    def nextList1(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)

    def nextList2(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_3)

    def nextList3(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_4)

    def backList(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.tab)

    def del_ingred1(self):
        del self.sps[self.sps.index(self.ui.ingred1.text())]
        self.ui.ingred1.setText('')
        self.ui.del1.hide()

    def del_ingred2(self):
        del self.sps[self.sps.index(self.ui.ingred2.text())]
        self.ui.ingred2.setText('')
        self.ui.del2.hide()

    def del_ingred3(self):
        del self.sps[self.sps.index(self.ui.ingred3.text())]
        self.ui.ingred3.setText('')
        self.ui.del3.hide()

    def del_ingred4(self):
        del self.sps[self.sps.index(self.ui.ingred4.text())]
        self.ui.ingred4.setText('')
        self.ui.del4.hide()

    def del_ingred5(self):
        del self.sps[self.sps.index(self.ui.ingred5.text())]
        self.ui.ingred5.setText('')
        self.ui.del5.hide()

    def ingredien(self):
        if len(self.ui.lineEdit.text()) > 0 and len(self.sps) < 5:
            self.sps.append(self.ui.lineEdit.text())
            x = self.ui.lineEdit.text()
            self.ui.lineEdit.setText('')
            if len(self.ui.ingred1.text()) == 0:
                self.ui.ingred1.setText(str(x))
                self.ui.del1.show()
            elif len(self.ui.ingred2.text()) == 0:
                self.ui.ingred2.setText(str(x))
                self.ui.del2.show()
            elif len(self.ui.ingred3.text()) == 0:
                self.ui.ingred3.setText(str(x))
                self.ui.del3.show()
            elif len(self.ui.ingred4.text()) == 0:
                self.ui.ingred4.setText(str(x))
                self.ui.del4.show()
            elif len(self.ui.ingred5.text()) == 0:
                self.ui.ingred5.setText(str(x))
                self.ui.del5.show()

    def bdinsert(self):
        global sqlite_connection
        self.name = self.ui.name4.text()
        self.type = self.ui.comboBox.currentText()
        if self.type == 'Завтрак':
            self.type = 1
        elif self.type == 'Закуски':
            self.type = 2
        elif self.type == 'Салаты':
            self.type = 3
        elif self.type == 'Первое блюдо':
            self.type = 4
        elif self.type == 'Второе блюдо':
            self.type = 5
        elif self.type == 'Десерт':
            self.type = 6
        self.ing = self.ui.inghred4.text()
        self.recip = self.ui.rec4.text()
        try:
            sqlite_connection = sqlite3.connect(f"{os.getcwd()}/recipe.sqlite")
            cursor = sqlite_connection.cursor()
            sqlite_insert_query = f"""INSERT INTO allthere
                    (name,type,recs,ingrediens) 
                    VALUES
                    ('{self.name}',{self.type},'{self.recip}','{self.ing}')"""
            count = cursor.execute(sqlite_insert_query)
            sqlite_connection.commit()
            cursor.close()


        except sqlite3.Error as error:
            pass
        finally:
            if sqlite_connection:
                sqlite_connection.close()

        self.ui.name4.setText('')
        self.ui.inghred4.setText('')
        self.ui.rec4.setText('')
        self.ui.label_13.setText(f'Вы успешно добавили {self.count} рецептов')
        self.count += 1

    def bdwork(self):
        self.ui.listWidget.clear()
        self.sets = set(self.sps)
        self.dct = {'type': [], 'osnova': set(self.sps)}
        if self.ui.type_cbox_0.isChecked() is True:
            self.dct['type'].append(1)
        if self.ui.type_cbox_1.isChecked() is True:
            self.dct['type'].append(2)
        if self.ui.type_cbox_2.isChecked() is True:
            self.dct['type'].append(3)
        if self.ui.type_cbox_3.isChecked() is True:
            self.dct['type'].append(4)
        if self.ui.type_cbox_4.isChecked() is True:
            self.dct['type'].append(5)
        if self.ui.type_cbox_5.isChecked() is True:
            self.dct['type'].append(6)
        if len(self.dct['type']) == 0 and len(self.dct['osnova']) == 0:
            self.ui.viewRecipe.setText(
                'Вы не выбрали ни одной категории, поэтому и не получили ни одного рецепта. '
                '\nДля того, чтобы их получить выберите нужные вам категории')
            self.ui.viewRecipe.setStyleSheet("""font: bold 20px""")
        else:
            self.ui.viewRecipe.setText('Вот какие рецепты мы сумели найти для вас:')
            self.ui.viewRecipe.setStyleSheet("""font: bold 30px""")
            self.res = []
            con = sqlite3.connect(f"{os.getcwd()}/recipe.sqlite")
            cur = con.cursor()
            for i in self.dct['type']:
                x = cur.execute(f"""select * from allthere where type = {i}""").fetchall()
                for i in x:
                    if len(self.sets & set(i[4].split(','))) == len(self.sets):
                        self.res.append(i)
            if len(self.res) > 0:
                lst = [[i[1], i[2]] for i in self.res]
                for i in range(len(lst)):
                    if lst[i][1] == 1:
                        lst[i][1] = 'Завтрак'
                    elif lst[i][1] == 2:
                        lst[i][1] = 'Закуски'
                    elif lst[i][1] == 3:
                        lst[i][1] = 'Салат'
                    elif lst[i][1] == 4:
                        lst[i][1] = 'Первое блюдо'
                    elif lst[i][1] == 5:
                        lst[i][1] = 'Второе блюдо'
                    elif lst[i][1] == 6:
                        lst[i][1] = 'Десерт'
                for i in range(len(lst)):
                    curind = self.ui.listWidget.currentRow()
                    self.ui.listWidget.insertItem(curind, f'{lst[i][0]} ({lst[i][1]})')

            else:
                self.ui.viewRecipe.setText('В нашей книге нет подходих рецептов.\nВыберите другие параметры.')
                self.ui.viewRecipe.setStyleSheet("""font: bold 20px""")

    def rnd_recipe(self):
        con = sqlite3.connect(f"{os.getcwd()}/recipe.sqlite")
        cur = con.cursor()
        try:
            result = cur.execute(
            '''SELECT id FROM allthere''').fetchall()
            result1 = random.sample([i[0] for i in result], 3)
            x = cur.execute(f'''select name,type,ingrediens from allthere
                                    where id = {result1[0]}''').fetchone()
            stroka = ''
            for i in x:
                if x.index(i) == len(x) - 1:
                    stroka += ('Ингредиенты: ' + str(i) + '\n')
                elif isinstance(i, str):
                    stroka += (str(i) + '\n')
                if isinstance(i, int):
                    if i == 1:
                        stroka += 'Завтрак\n'
                    elif i == 2:
                        stroka += 'Закуски\n'
                    elif i == 3:
                        stroka += 'Салаты\n'
                    elif i == 4:
                        stroka += 'Первое блюдо\n'
                    elif i == 5:
                        stroka += 'Второе блюдо\n'
                    elif i == 6:
                        stroka += 'Десерт\n'
            self.ui.viewRecipe3.setText(stroka)
            self.ui.viewRecipe3.setWordWrap(True)
            self.ui.viewRecipe3.setAlignment(
                QtCore.Qt.AlignCenter
            )
            self.ui.viewRecipe3.setStyleSheet("font: 20pt \"Georgia\";")
        except sqlite3.OperationalError:
            result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            print(result)

    def openWindow1(self):
        self.item = self.ui.listWidget.currentRow()
        self.itemmm = self.ui.listWidget.item(self.item)
        if self.itemmm is not None:
            con = sqlite3.connect(f"{os.getcwd()}/recipe.sqlite")
            cur = con.cursor()
            x = cur.execute(f'''select * from allthere
                                            where name = "{self.itemmm.text().split(' (')[0]}"''').fetchone()
            stroka, flag = '', False
            for i in x:
                if x.index(i) == len(x) - 1:
                    stroka += ('Ингредиенты: ' + str(i) + '\n')
                elif isinstance(i, str):
                    stroka += (str(i) + '\n')
                if isinstance(i, int):
                    if flag is False:
                        flag = True
                    else:
                        if i == 1:
                            stroka += 'Завтрак\n'
                        elif i == 2:
                            stroka += 'Закуски\n'
                        elif i == 3:
                            stroka += 'Салаты\n'
                        elif i == 4:
                            stroka += 'Первое блюдо\n'
                        elif i == 5:
                            stroka += 'Второе блюдо\n'
                        elif i == 6:
                            stroka += 'Десерт\n'

            self.w2 = Window2(self)
            self.w2.show()
            self.w2.label123123.setText(f'{stroka}')
        else:
            self.ui.viewRecipe.setText('Вы не выбрали ни одного рецепта для того,\n чтобы открыть его в новом окне.')
            self.ui.viewRecipe.setStyleSheet("""font: bold 20px""")

    def openWindow2(self):
        con = sqlite3.connect(f"{os.getcwd()}/recipe.sqlite")
        cur = con.cursor()
        self.txt = self.ui.viewRecipe3.text().split('\n')[0]
        x = cur.execute(f'''select * from allthere
                            where name = "{self.txt}"''').fetchone()
        stroka, flag = '', False
        for i in x:
            if x.index(i) == len(x) - 1:
                stroka += ('Ингредиенты: ' + str(i) + '\n')
            elif isinstance(i, str):
                stroka += (str(i) + '\n')
            if isinstance(i, int):
                if flag is False:
                    flag = True
                else:
                    if i == 1:
                        stroka += 'Завтрак\n'
                    elif i == 2:
                        stroka += 'Закуски\n'
                    elif i == 3:
                        stroka += 'Салаты\n'
                    elif i == 4:
                        stroka += 'Первое блюдо\n'
                    elif i == 5:
                        stroka += 'Второе блюдо\n'
                    elif i == 6:
                        stroka += 'Десерт\n'

        self.w22 = Window2(self)
        self.w22.show()
        self.w22.label123123.setText(f'{stroka}')


class Window2(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.parent = parent
        self.setGeometry(250, 55, 1000, 800)
        self.setWindowTitle('Рецепт')
        self.label123123 = QLabel(self)
        self.label123123.setGeometry(0, 0, 1000, 800)
        self.label123123.setWordWrap(True)
        self.label123123.setAlignment(
            QtCore.Qt.AlignCenter
        )
        self.label123123.setStyleSheet("font: 20pt \"Georgia\";"
                                       "background-color: rgb(223, 175, 98);")


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(-20, -30, 1300, 850))
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setStyleSheet("background-color: rgb(223, 175, 98);")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setStyleSheet("")
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(310, 90, 1221, 261))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 48pt \"Georgia\";\n"
                                 "background-color: transparent;")
        self.label.setObjectName("label")
        self.t1Button1 = QtWidgets.QPushButton(self.tab)
        self.t1Button1.setGeometry(QtCore.QRect(430, 390, 400, 80))
        self.t1Button1.setStyleSheet(" #t1Button1 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t1Button1:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t1Button1.setObjectName("t1Button1")
        self.t1Button2 = QtWidgets.QPushButton(self.tab)
        self.t1Button2.setGeometry(QtCore.QRect(430, 500, 401, 81))
        self.t1Button2.setStyleSheet(" #t1Button2 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t1Button2:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t1Button2.setObjectName("t1Button2")
        self.fon = QtWidgets.QLabel(self.tab)
        self.fon.setGeometry(QtCore.QRect(10, 0, 1901, 1211))
        self.fon.setStyleSheet("background-color: rgb(223, 175, 98);")
        self.fon.setText("")
        self.fon.setObjectName("fon")
        self.t1Button3 = QtWidgets.QPushButton(self.tab)
        self.t1Button3.setGeometry(QtCore.QRect(430, 610, 400, 80))
        self.t1Button3.setStyleSheet(" #t1Button3 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t1Button3:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t1Button3.setObjectName("t1Button3")
        self.fon.raise_()
        self.label.raise_()
        self.t1Button1.raise_()
        self.t1Button2.raise_()
        self.t1Button3.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setStyleSheet("background-color: rgb(223, 175, 98);")
        self.tab_2.setObjectName("tab_2")
        self.line = QtWidgets.QFrame(self.tab_2)
        self.line.setGeometry(QtCore.QRect(340, -20, 20, 841))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(110, 130, 182, 233))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.typeLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.typeLayout.setContentsMargins(0, 0, 0, 0)
        self.typeLayout.setObjectName("typeLayout")
        self.type_cbox_0 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.type_cbox_0.setStyleSheet("font: 11pt \"Georgia\";")
        self.type_cbox_0.setObjectName("type_cbox_0")
        self.typeLayout.addWidget(self.type_cbox_0)
        self.type_cbox_1 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.type_cbox_1.setStyleSheet("font: 11pt \"Georgia\";")
        self.type_cbox_1.setObjectName("type_cbox_1")
        self.typeLayout.addWidget(self.type_cbox_1)
        self.type_cbox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.type_cbox_2.setStyleSheet("font: 11pt \"Georgia\";")
        self.type_cbox_2.setObjectName("type_cbox_2")
        self.typeLayout.addWidget(self.type_cbox_2)
        self.type_cbox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.type_cbox_3.setStyleSheet("font: 11pt \"Georgia\";")
        self.type_cbox_3.setObjectName("type_cbox_3")
        self.typeLayout.addWidget(self.type_cbox_3)
        self.type_cbox_4 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.type_cbox_4.setStyleSheet("font: 11pt \"Georgia\";")
        self.type_cbox_4.setObjectName("type_cbox_4")
        self.typeLayout.addWidget(self.type_cbox_4)
        self.type_cbox_5 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.type_cbox_5.setStyleSheet("font: 11pt \"Georgia\";")
        self.type_cbox_5.setObjectName("type_cbox_5")
        self.typeLayout.addWidget(self.type_cbox_5)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(50, 20, 301, 71))
        self.label_4.setStyleSheet("font: 14pt \"Georgia\";\n"
                                   "background-color: transparent;")
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(50, 90, 281, 41))
        self.label_6.setStyleSheet("background-color: transparent;\n"
                                   "font: bold 14px;")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(50, 350, 281, 41))
        self.label_7.setStyleSheet("background-color: transparent;\n"
                                   "font: bold 14px;")
        self.label_7.setObjectName("label_7")
        self.t2Button1 = QtWidgets.QPushButton(self.tab_2)
        self.t2Button1.setGeometry(QtCore.QRect(50, 680, 286, 61))
        self.t2Button1.setStyleSheet(" #t2Button1 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t2Button1:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t2Button1.setObjectName("t2Button1")
        self.viewRecipe = QtWidgets.QLabel(self.tab_2)
        self.viewRecipe.setGeometry(QtCore.QRect(360, 10, 851, 81))
        self.viewRecipe.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.viewRecipe.setStyleSheet("font: 32pt \"Georgia\";")
        self.viewRecipe.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.viewRecipe.setObjectName("viewRecipe")
        self.t2Button2 = QtWidgets.QPushButton(self.tab_2)
        self.t2Button2.setGeometry(QtCore.QRect(1070, 710, 141, 41))
        self.t2Button2.setStyleSheet(" #t2Button2 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t2Button2:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t2Button2.setObjectName("t2Button2")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(40, 440, 241, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.t2Button3 = QtWidgets.QPushButton(self.tab_2)
        self.t2Button3.setGeometry(QtCore.QRect(290, 440, 51, 31))
        self.t2Button3.setStyleSheet(" #t2Button3 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 20px;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t2Button3:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t2Button3.setObjectName("t2Button3")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(40, 380, 281, 51))
        self.label_2.setStyleSheet("font: 10pt \"Georgia\";\n"
                                   "background-color: transparent;")
        self.label_2.setObjectName("label_2")
        self.ingred1 = QtWidgets.QLabel(self.tab_2)
        self.ingred1.setGeometry(QtCore.QRect(40, 490, 241, 21))
        self.ingred1.setText("")
        self.ingred1.setObjectName("ingred1")
        self.ingred2 = QtWidgets.QLabel(self.tab_2)
        self.ingred2.setGeometry(QtCore.QRect(40, 520, 241, 21))
        self.ingred2.setText("")
        self.ingred2.setObjectName("ingred2")
        self.ingred3 = QtWidgets.QLabel(self.tab_2)
        self.ingred3.setGeometry(QtCore.QRect(40, 550, 241, 21))
        self.ingred3.setText("")
        self.ingred3.setObjectName("ingred3")
        self.ingred4 = QtWidgets.QLabel(self.tab_2)
        self.ingred4.setGeometry(QtCore.QRect(40, 580, 241, 21))
        self.ingred4.setText("")
        self.ingred4.setObjectName("ingred4")
        self.ingred5 = QtWidgets.QLabel(self.tab_2)
        self.ingred5.setGeometry(QtCore.QRect(40, 610, 241, 21))
        self.ingred5.setText("")
        self.ingred5.setObjectName("ingred5")
        self.del1 = QtWidgets.QPushButton(self.tab_2)
        self.del1.setGeometry(QtCore.QRect(290, 490, 31, 21))
        self.del1.setStyleSheet(" #del1 {\n"
                                "     background-color:rgb(73, 105, 146);\n"
                                "     border-style: outset;\n"
                                "     color: rgb(255, 255, 255);\n"
                                "     border-width: 2px;\n"
                                "     border-radius: 10px;\n"
                                "     border-color: beige;\n"
                                "     font: bold 11px;\n"
                                "     padding: 6px;\n"
                                " }\n"
                                " #del1:pressed {\n"
                                "     background-color:rgb(44, 79, 120); \n"
                                "     border-style: inset;\n"
                                " }\n"
                                "")
        self.del1.setObjectName("del1")
        self.del2 = QtWidgets.QPushButton(self.tab_2)
        self.del2.setGeometry(QtCore.QRect(290, 520, 31, 21))
        self.del2.setStyleSheet(" #del2 {\n"
                                "     background-color:rgb(73, 105, 146);\n"
                                "     border-style: outset;\n"
                                "     color: rgb(255, 255, 255);\n"
                                "     border-width: 2px;\n"
                                "     border-radius: 10px;\n"
                                "     border-color: beige;\n"
                                "     font: bold 11px;\n"
                                "     padding: 6px;\n"
                                " }\n"
                                " #del2:pressed {\n"
                                "     background-color:rgb(44, 79, 120); \n"
                                "     border-style: inset;\n"
                                " }\n"
                                "")
        self.del2.setObjectName("del2")
        self.del3 = QtWidgets.QPushButton(self.tab_2)
        self.del3.setGeometry(QtCore.QRect(290, 550, 31, 21))
        self.del3.setStyleSheet(" #del3 {\n"
                                "     background-color:rgb(73, 105, 146);\n"
                                "     border-style: outset;\n"
                                "     color: rgb(255, 255, 255);\n"
                                "     border-width: 2px;\n"
                                "     border-radius: 10px;\n"
                                "     border-color: beige;\n"
                                "     font: bold 11px;\n"
                                "     padding: 6px;\n"
                                " }\n"
                                " #del3:pressed {\n"
                                "     background-color:rgb(44, 79, 120); \n"
                                "     border-style: inset;\n"
                                " }\n"
                                "")
        self.del3.setObjectName("del3")
        self.del4 = QtWidgets.QPushButton(self.tab_2)
        self.del4.setGeometry(QtCore.QRect(290, 580, 31, 21))
        self.del4.setStyleSheet(" #del4 {\n"
                                "     background-color:rgb(73, 105, 146);\n"
                                "     border-style: outset;\n"
                                "     color: rgb(255, 255, 255);\n"
                                "     border-width: 2px;\n"
                                "     border-radius: 10px;\n"
                                "     border-color: beige;\n"
                                "     font: bold 11px;\n"
                                "     padding: 6px;\n"
                                " }\n"
                                " #del4:pressed {\n"
                                "     background-color:rgb(44, 79, 120); \n"
                                "     border-style: inset;\n"
                                " }\n"
                                "")
        self.del4.setObjectName("del4")
        self.del5 = QtWidgets.QPushButton(self.tab_2)
        self.del5.setGeometry(QtCore.QRect(290, 610, 31, 21))
        self.del5.setStyleSheet(" #del5 {\n"
                                "     background-color:rgb(73, 105, 146);\n"
                                "     border-style: outset;\n"
                                "     color: rgb(255, 255, 255);\n"
                                "     border-width: 2px;\n"
                                "     border-radius: 10px;\n"
                                "     border-color: beige;\n"
                                "     font: bold 11px;\n"
                                "     padding: 6px;\n"
                                " }\n"
                                " #del5:pressed {\n"
                                "     background-color:rgb(44, 79, 120); \n"
                                "     border-style: inset;\n"
                                " }\n"
                                "")
        self.del5.setObjectName("del5")
        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setGeometry(QtCore.QRect(375, 91, 811, 561))
        self.listWidget.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
                                      "text-decoration: underline;")
        self.listWidget.setObjectName("listWidget")
        self.t2Button4 = QtWidgets.QPushButton(self.tab_2)
        self.t2Button4.setGeometry(QtCore.QRect(390, 680, 286, 61))
        self.t2Button4.setStyleSheet(" #t2Button4 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t2Button4:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t2Button4.setObjectName("t2Button4")
        self.viewRecipe.raise_()
        self.line.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.label_4.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.t2Button1.raise_()
        self.t2Button2.raise_()
        self.lineEdit.raise_()
        self.t2Button3.raise_()
        self.label_2.raise_()
        self.ingred1.raise_()
        self.ingred2.raise_()
        self.ingred3.raise_()
        self.ingred4.raise_()
        self.ingred5.raise_()
        self.del1.raise_()
        self.del2.raise_()
        self.del3.raise_()
        self.del4.raise_()
        self.del5.raise_()
        self.listWidget.raise_()
        self.t2Button4.raise_()
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setStyleSheet("background-color: rgb(223, 175, 98);")
        self.tab_3.setObjectName("tab_3")
        self.t3Button1 = QtWidgets.QPushButton(self.tab_3)
        self.t3Button1.setGeometry(QtCore.QRect(920, 40, 286, 71))
        self.t3Button1.setStyleSheet(" #t3Button1 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t3Button1:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t3Button1.setObjectName("t3Button1")
        self.viewRecipe3 = QtWidgets.QLabel(self.tab_3)
        self.viewRecipe3.setGeometry(QtCore.QRect(60, 30, 831, 701))
        self.viewRecipe3.setText("")
        self.viewRecipe3.setObjectName("viewRecipe3")
        self.t3Button2 = QtWidgets.QPushButton(self.tab_3)
        self.t3Button2.setGeometry(QtCore.QRect(920, 130, 286, 71))
        self.t3Button2.setStyleSheet(" #t3Button2 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t3Button2:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t3Button2.setObjectName("t3Button2")
        self.t3Button3 = QtWidgets.QPushButton(self.tab_3)
        self.t3Button3.setGeometry(QtCore.QRect(1040, 700, 151, 51))
        self.t3Button3.setStyleSheet(" #t3Button3 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t3Button3:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t3Button3.setObjectName("t3Button3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.t4Button1 = QtWidgets.QPushButton(self.tab_4)
        self.t4Button1.setGeometry(QtCore.QRect(450, 500, 371, 71))
        self.t4Button1.setStyleSheet(" #t4Button1 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     min-width: 10em;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t4Button1:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t4Button1.setObjectName("t4Button1")
        self.label_5 = QtWidgets.QLabel(self.tab_4)
        self.label_5.setGeometry(QtCore.QRect(220, 330, 56, 16))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_11 = QtWidgets.QLabel(self.tab_4)
        self.label_11.setGeometry(QtCore.QRect(250, 30, 791, 181))
        self.label_11.setStyleSheet("font: 45pt \"Georgia\";\n"
                                    "background-color: transparent;")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_4)
        self.label_12.setGeometry(QtCore.QRect(890, 340, 301, 41))
        self.label_12.setStyleSheet("font: 15pt \"Georgia\";\n"
                                    "background-color: transparent;")
        self.label_12.setObjectName("label_12")
        self.t4Button2 = QtWidgets.QPushButton(self.tab_4)
        self.t4Button2.setGeometry(QtCore.QRect(450, 600, 371, 71))
        self.t4Button2.setStyleSheet(" #t4Button2 {\n"
                                     "     background-color:rgb(73, 105, 146);\n"
                                     "     border-style: outset;\n"
                                     "     color: rgb(255, 255, 255);\n"
                                     "     border-width: 2px;\n"
                                     "     border-radius: 10px;\n"
                                     "     border-color: beige;\n"
                                     "     font: bold 22px;\n"
                                     "     padding: 6px;\n"
                                     " }\n"
                                     " #t4Button2:pressed {\n"
                                     "     background-color:rgb(44, 79, 120); \n"
                                     "     border-style: inset;\n"
                                     " }\n"
                                     "")
        self.t4Button2.setObjectName("t4Button2")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab_4)
        self.formLayoutWidget.setGeometry(QtCore.QRect(340, 250, 541, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setStyleSheet("font: 20pt \"Georgia\";\n"
                                   "background-color: transparent;")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setStyleSheet("font: 20pt \"Georgia\";\n"
                                   "background-color: transparent;")
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_9.setStyleSheet("font: 20pt \"Georgia\";\n"
                                   "background-color: transparent;")
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_10.setStyleSheet("font: 20pt \"Georgia\";\n"
                                    "background-color: transparent;")
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setStyleSheet(" #comboBox {\n"
                                    "     background-color:rgb(73, 105, 146);\n"
                                    "     border-style: outset;\n"
                                    "     color: rgb(255, 255, 255);\n"
                                    "     border-width: 2px;\n"
                                    "     border-radius: 10px;\n"
                                    "     border-color: beige;\n"
                                    "     font: bold 22px;\n"
                                    "\n"
                                    "     padding: 6px;\n"
                                    " }\n"
                                    " #comboBox:pressed {\n"
                                    "     background-color:rgb(44, 79, 120); \n"
                                    "     border-style: inset;\n"
                                    " }\n"
                                    "")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.name4 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.name4.setObjectName("name4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name4)
        self.rec4 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec4.setObjectName("rec4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rec4)
        self.inghred4 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.inghred4.setObjectName("inghred4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.inghred4)
        self.label_13 = QtWidgets.QLabel(self.tab_4)
        self.label_13.setGeometry(QtCore.QRect(40, 510, 401, 61))
        self.label_13.setStyleSheet("font: 15pt \"Georgia\";\n"
                                    "background-color: transparent;")
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.tabWidget.addTab(self.tab_4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "   Электронная\n"
                                                    "кулинарная книга"))
        self.t1Button1.setText(_translate("MainWindow", "Поиск рецепта"))
        self.t1Button2.setText(_translate("MainWindow", "Случайный рецепт"))
        self.t1Button3.setText(_translate("MainWindow", "Добавить рецепт"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.type_cbox_0.setText(_translate("MainWindow", "Завтрак"))
        self.type_cbox_1.setText(_translate("MainWindow", "Закуски"))
        self.type_cbox_2.setText(_translate("MainWindow", "Салаты"))
        self.type_cbox_3.setText(_translate("MainWindow", "Первые блюда"))
        self.type_cbox_4.setText(_translate("MainWindow", "Вторые блюда"))
        self.type_cbox_5.setText(_translate("MainWindow", "Десерты"))
        self.label_4.setText(_translate("MainWindow", "Вид рецепта, который вы\n"
                                                      " бы хотели приготовить:"))
        self.label_6.setText(_translate("MainWindow", "Рецепты по типу блюд:"))
        self.label_7.setText(_translate("MainWindow", "Рецепты блюд по ингредиентам:"))
        self.t2Button1.setText(_translate("MainWindow", "Получить рецепты"))
        self.viewRecipe.setText(
            _translate("MainWindow", "<html><head/><body><p>Выберите категории для рецетов</p></body></html>"))
        self.t2Button2.setText(_translate("MainWindow", "Вернуться"))
        self.t2Button3.setText(_translate("MainWindow", "Ok"))
        self.label_2.setText(_translate("MainWindow", "Пишите ингредиенты в начальной\n"
                                                      " форме и в единственном числе"))
        self.del1.setText(_translate("MainWindow", "X"))
        self.del2.setText(_translate("MainWindow", "X"))
        self.del3.setText(_translate("MainWindow", "X"))
        self.del4.setText(_translate("MainWindow", "X"))
        self.del5.setText(_translate("MainWindow", "X"))
        self.t2Button4.setText(_translate("MainWindow", "Открыть в другом окне"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.t3Button1.setText(_translate("MainWindow", "Другое блюдо"))
        self.t3Button2.setText(_translate("MainWindow", "Открыть в другом окне"))
        self.t3Button3.setText(_translate("MainWindow", "Вернуться"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Страница"))
        self.t4Button1.setText(_translate("MainWindow", "Добавить рецепт"))
        self.label_11.setText(_translate("MainWindow", "Добавьте свой рецепт"))
        self.label_12.setText(_translate("MainWindow", "*Запишите их через \",\""))
        self.t4Button2.setText(_translate("MainWindow", "Вернуться"))
        self.label_3.setText(_translate("MainWindow", "Название:"))
        self.label_8.setText(_translate("MainWindow", "Тип блюда:"))
        self.label_9.setText(_translate("MainWindow", "Ингредиенты:"))
        self.label_10.setText(_translate("MainWindow", "Рецепт:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Завтрак"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Закуски"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Салаты"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Первое блюдо"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Второе блюдо"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Десерты"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Страница"))


def app():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


app()
