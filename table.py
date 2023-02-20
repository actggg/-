import re  # Регулярные выражения.
import sys
import nltk
import requests  # Загрузка новостей с сайта.
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QTableWidget, QTableWidgetItem
from bs4 import BeautifulSoup
from collections import Counter
from prediction import pred

import statistics
from statistics import mode


def know_text_in_link(link):
    resp = requests.get(link)
    # Загружаем текст в объект типа BeautifulSoup.
    bs = BeautifulSoup(resp.text, "html5lib")
    # Получаем заголовок статьи.
    if bs.h1:
        aTitle = bs.h1.text.replace("\xa0", " ")
        # Получаем текст статьи.
        findheaders = re.compile("<output+?>", re.S)
        anArticle = BeautifulSoup(" ".join([p.text for p in bs.find_all("p")]), "html5lib").get_text().replace("\xa0",
                                                                                                               " ")
        anArticle = anArticle.replace('↑', '')
        return anArticle
    return 0


classes = ['business', 'entertainment', 'politics', 'medical', 'graphics', 'historical', 'food', 'space', 'sport',
           'technologie']
for i in pred([str(know_text_in_link(
        'https://www.theguardian.com/business/2023/feb/14/us-inflation-eases-seventh-consecutive-month'))]):
    print(classes[i])

try:
    class MainWidget(QMainWindow):
        def __init__(self):
            super().__init__()
            uic.loadUi('untitled.ui', self)
            self.text_button.clicked.connect(self.text_helper)
            self.link_button.clicked.connect(self.link_helper)
            self.file_button.clicked.connect(self.file_helper)
            nltk.download("stopwords")  # поддерживает удаление стоп-слов
            nltk.download('punkt')  # делит текст на список предложений
            nltk.download('wordnet')  # проводит лемматизацию
            nltk.download('omw-1.4')

        def file_helper(self):
            print(3)
            with open(self.file_input.text(), 'r', encoding='utf8') as f:
                k = f.read().split()
                s = []
                for i in k:
                    print(i)
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
            rist = [classes[pred([str(know_text_in_link(self.link_input.text()))])[0]], classes[pred([str(know_text_in_link(self.link_input.text()))])[1]], classes[pred([str(know_text_in_link(self.link_input.text()))])[2]]]
            print(rist)
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
            '''
            print(2222)
            print(pred['eeeee'])
            rist = [classes[pred([str(self.text_input.toPlainText())])[0]],
                    classes[pred([str(self.text_input.toPlainText())])[1]],
                    classes[pred([str(self.text_input.toPlainText())])[2]]]
            print(rist)
            if rist.count(mode(rist)) != 1:
                t = mode(rist)
            else:
                t = '-'
            '''
            p = pred([str(self.text_input.toPlainText())])[0]
            p2 = pred([str(self.text_input.toPlainText())])[1]
            p3 = pred([str(self.text_input.toPlainText())])[2]
            rist = [p,
                    p2,
                    p3]
            print(rist)
            if rist.count(mode(rist)) > 1:
                print(mode(rist))
                t = classes[mode(rist)]
                print(t)
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

            self.setMinimumSize(QSize(600, 200))  # Set sizes
            self.setWindowTitle("Работа с QTableWidget")  # Set the window title
            central_widget = QWidget(self)  # Create a central widget
            self.setCentralWidget(central_widget)  # Install the central widget

            grid_layout = QGridLayout(self)  # Create QGridLayout
            central_widget.setLayout(grid_layout)  # Set this layout in central widget

            table = QTableWidget(self)  # Create a table
            table.setColumnCount(5)  # Set three columns
            table.setRowCount(len(metods))  # and one row

            # Set the table headers
            table.setHorizontalHeaderLabels(["link", "Method 1", "Method 2", "Method 3", 'sum'])

            # Set the tooltips to headings
            table.horizontalHeaderItem(1).setToolTip("Column 1 ")
            table.horizontalHeaderItem(2).setToolTip("Column 2 ")
            table.horizontalHeaderItem(3).setToolTip("Column 3 ")
            table.horizontalHeaderItem(4).setToolTip("sum")

            # Set the alignment to the headers
            table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
            table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
            table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
            for i in range(len(metods)):
                table.setItem(i, 0, QTableWidgetItem(metods[i]['link']))
                table.setItem(i, 1, QTableWidgetItem(metods[i]['Method_1']))
                table.setItem(i, 2, QTableWidgetItem(metods[i]['Method_2']))
                table.setItem(i, 3, QTableWidgetItem(metods[i]['Method_3']))
                table.setItem(i, 4, QTableWidgetItem(metods[i]['sum']))


            # Do the resize of the columns by content
            '''
            table.resizeColumnsToContents()
            self.btn = QPushButton('Сохранить', self)
            self.btn.resize(150, 50)
            self.btn.move(100, 50)
            '''

            grid_layout.addWidget(table, 500, 200)  # Adding the table to the grid
except Exception as e:
    print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())
