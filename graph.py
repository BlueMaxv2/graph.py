import sqlite3
import sys
import math
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
import matplotlib.pyplot as plt

#Класс основного окна
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('1.ui', self)
        equat = 0
        self.pushButton.clicked.connect(self.calculate)

#Функция получающая и обрабатывающая данные
    def calculate(self):
        #Подключение к базе данных
        con = sqlite3.connect('ranges.sqlite3')
        cur = con.cursor()
        #Очистка
        cur.execute('DELETE from xranges')
        cur.execute('DELETE from yranges')
        con.commit()
        #Ограничения получаются из строки и записываются
        equat = self.lineEdit.text()
        xrange = self.lineEdit_2.text().split(' ')
        #Полученное выражение редактируется
        if 'log' in equat:
            equat = equat.replace('log', 'math.log')
        if 'sin' in equat:
            equat = equat.replace('sin', 'math.sin')
        if 'cos' in equat:
            equat = equat.replace('cos', 'math.cos')
        if 'ctg' in equat:
            equat = equat.replace('ctg', '1 / math.tan')
        if 'tg' in equat:
            equat = equat.replace('tg', 'math.tan')
        if 'deg' in equat:
            equat = equat.replace('deg', 'math.radians')
        if 'pi' in equat:
            equat = equat.replace('pi', 'math.pi')
        for i in range(len(xrange)):
            xrange[i] = int(xrange[i])
        yrange = equat
        #Значения записываются в базу данных
        for i in range(len(xrange)):
            cur.execute(f'INSERT INTO xranges(xranges) values({xrange[i]})')
        cur.execute(f"INSERT INTO yranges(yranges) values('{yrange}')")
        con.commit()
        x = np.linspace(xrange[0], xrange[1], 100)
        y = []
        for i in x:
            y.append(eval(yrange.replace('x', f'{i}')))
        #Выводится график
        fig, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec())
