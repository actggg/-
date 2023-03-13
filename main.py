import re  # Регулярные выражения.
import sys
from statistics import mode
from urllib.request import urlopen
import nltk
import requests  # Загрузка новостей с сайта.
from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QTableWidget, QTableWidgetItem
from bs4 import BeautifulSoup
import sqlite3

from prediction import pred


def know_text_in_link(link):
    resp = requests.get(link)
    if 300 > resp.status_code >= 200:
        html = urlopen(link).read()
        soup = BeautifulSoup(html, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    return f'Ошибка программы {resp.status_code}'


classes = ['business', 'entertainment', 'politics', 'medical', 'graphics', 'historical', 'food', 'space', 'sport',
           'technologie']


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.setWindowTitle("Классификатор по тематикам")
        self.text_button.clicked.connect(self.text_helper)
        self.link_button.clicked.connect(self.link_helper)
        self.file_button.clicked.connect(self.file_helper)
        self.setFixedSize(800, 560)
        nltk.download("stopwords")  # поддерживает удаление стоп-слов
        nltk.download('punkt')  # делит текст на список предложений
        nltk.download('wordnet')  # проводит лемматизацию
        nltk.download('omw-1.4')

    def file_helper(self):
        with open(self.file_input.text(), 'r', encoding='utf8') as f:
            k = f.read().split()
            r = 0
            s = []
            for i in k:
                r += 1
                print(f'Обрабатывает ссылку номер {r}')
                if know_text_in_link(i) != 0:
                    rist = [classes[pred([str(know_text_in_link(i))])[0]],
                            classes[pred([str(know_text_in_link(i))])[1]],
                            classes[pred([str(know_text_in_link(i))])[2]]]
                    if rist.count(mode(rist)) != 1:
                        t = mode(rist)
                    else:
                        t = '-'
                    method_class = {'link': i,
                                    'Method_1': classes[pred([str(know_text_in_link(i))])[0]],
                                    'Method_2': classes[pred([str(know_text_in_link(i))])[1]],
                                    'Method_3': classes[pred([str(know_text_in_link(i))])[2]],
                                    'sum': t}
                    s.append(method_class)
            self.table = Table(s)
            self.table.show()

    def link_helper(self):
        s = []
        rist = [classes[pred([str(know_text_in_link(self.link_input.text()))])[0]],
                classes[pred([str(know_text_in_link(self.link_input.text()))])[1]],
                classes[pred([str(know_text_in_link(self.link_input.text()))])[2]]]
        if rist.count(mode(rist)) != 1:
            t = mode(rist)
        else:
            t = '-'
        method_class = {'link': self.link_input.text(),
                        'Method_1': classes[pred([str(know_text_in_link(self.link_input.text()))])[0]],
                        'Method_2': classes[pred([str(know_text_in_link(self.link_input.text()))])[1]],
                        'Method_3': classes[pred([str(know_text_in_link(self.link_input.text()))])[2]],
                        'sum': t}
        s.append(method_class)
        self.table = Table(s)
        self.table.show()

    def text_helper(self):
        p = pred([str(self.text_input.toPlainText())])[0]
        p2 = pred([str(self.text_input.toPlainText())])[1]
        p3 = pred([str(self.text_input.toPlainText())])[2]
        rist = [p,
                p2,
                p3]
        if rist.count(mode(rist)) > 1:
            t = classes[mode(rist)]
        else:
            t = '-'
        method_class = {'link': self.text_input.toPlainText(),
                        'Method_1': classes[p],
                        'Method_2': classes[p2],
                        'Method_3': classes[p3],
                        'sum': str(t)
                        }
        self.table = Table([method_class])
        self.table.show()


class Table(QMainWindow):
    # Override class constructor
    def __init__(self, metods):
        # You must call the super class method
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(650, 100 + len(metods) * 50))  # Set sizes
        self.setWindowTitle("Результаты с классификацией")  # Set the window title
        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Install the central widget

        grid_layout = QGridLayout(self)  # Create QGridLayout
        central_widget.setLayout(grid_layout)  # Set this layout in central widget

        self.table = QTableWidget(self)  # Create a table
        self.table.setColumnCount(6)  # Set three columns
        self.table.setRowCount(len(metods))  # and one row

        # Set the table headers
        self.table.setHorizontalHeaderLabels(["Адрес/текст", "GaussianNB", "SVM", "LogReg", 'Итого:', 'Редакция'])

        # Set the tooltips to headings
        self.table.horizontalHeaderItem(1).setToolTip("Column 1 ")
        self.table.horizontalHeaderItem(2).setToolTip("Column 2 ")
        self.table.horizontalHeaderItem(3).setToolTip("Column 3 ")
        self.table.horizontalHeaderItem(4).setToolTip("sum")

        # Set the alignment to the headers
        for i in range(len(metods)):
            self.table.setItem(i, 0, QTableWidgetItem(metods[i]['link']))
            self.table.setItem(i, 1, QTableWidgetItem(metods[i]['Method_1']))
            self.table.setItem(i, 2, QTableWidgetItem(metods[i]['Method_2']))
            self.table.setItem(i, 3, QTableWidgetItem(metods[i]['Method_3']))
            self.table.setItem(i, 4, QTableWidgetItem(metods[i]['sum']))
            self.table.setItem(i, 5, QTableWidgetItem('-'))

        self.table.resizeColumnsToContents()
        self.label = QLabel(self)
        self.label.setText(
            "В случае неверного ответа, поставте в поле 'Редакция' верный вариант и нажмите кнопку сохранить.")
        self.label.resize(700, 50)
        self.label.move(40, len(metods) * 36 + 42)
        #self.label2.setText(
         #   "Варианты: business, entertainment, politics, medical, graphics, historical, food, space, sport, technologie")
        #self.label2.resize(700, 50)
        #self.label2.move(40, len(metods) * 36 + 52)
        self.btn = QPushButton('Сохранить результат', self)
        self.btn.resize(150, 50)
        self.btn.move(40, len(metods) * 36 + 92)
        self.btn.clicked.connect(self.save)
        grid_layout.addWidget(self.table, 650, 100 + len(metods) * 50)  # Adding the table to the grid

    def save(self):
        classess = {'business': 1, 'entertainment': 2,
                   'politics': 3, 'medical': 4,
                   'graphics': 5, 'historical': 6,
                   'food': 7, 'space': 8,
                   'sport': 9, 'technologie': 10}
        cols = self.table.columnCount()
        for i in range(cols):
            if self.table.item(i, 0):
                if self.table.item(i, 5).text() != '-' and self.table.item(i, 5).text() in classes:
                    if 'http' in self.table.item(i, 0).text():
                        text = know_text_in_link(self.table.item(i, 0).text())
                    else:
                        text = self.table.item(i, 0).text()
                    if self.table.item(i, 5).text() in classes:
                        con = sqlite3.connect("database.db")
                        cursor = con.cursor()
                        cursor.execute("INSERT INTO [set](content, class) VALUES(?, ?)", (text, classess[self.table.item(i, 5).text()]))
                        con.commit()
                        cursor.close()
                        con.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())
