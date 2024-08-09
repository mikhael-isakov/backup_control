design_origin = '.py'
if design_origin == '.py':
    from design import Ui_MainWindow
import os, sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from hashlib import md5
from threading import Thread
import functions as funcs
from classes import date_time



class MainWindow(QMainWindow):
    #
    resized = QtCore.pyqtSignal()
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)
    #
    def __init__(self):
        #
        super(MainWindow, self).__init__()
        #
        if design_origin == '.py':
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
        elif design_origin == '.ui':
            self.ui = uic.loadUi(os.path.join(os.getcwd(), 'design.ui'), self)
        #
        funcs.set_window_sizes(self)
        funcs.set_main_ico_and_title(self)
        funcs.set_fonts(self)
        funcs.set_menu_icons(self)
        funcs.set_buttons_hover_properties(self)
        #
        # пусть кнопка "остановить проверку" вначале неактивна 
        self.ui.pushButton_4.setEnabled(False)
        #
        # установка функциональности пунктов меню 'Файл'
        self.ui.action_File_1.triggered.connect(self.select_origin_directory)
        self.ui.action_File_2.triggered.connect(self.select_synchr_directory)
        self.ui.action_File_3.triggered.connect(self.compare_directories)
        self.ui.action_File_4.triggered.connect(lambda: os._exit(0))
        #
        # установка функциональности пунктов меню 'Справка'
        text_1 = 'Программа совершает рекурсивный обход\nуказанных каталогов,\nи сравнивает хеши MD5 файлов\n'
        self.ui.action_Help_1.triggered.connect(lambda: self.show_popup_window(title='О программе', text=text_1))
        text_2_1 = 'При бэкапе методом синхронизации\nпри добавлении, изменении, или удалении\n'
        text_2_2 = 'файлов в исходном каталоге\nтакие же изменения происходят и в конечном\n(синхронизированном) каталоге'
        text_2 = text_2_1+text_2_2
        self.ui.action_Help_2.triggered.connect(lambda: self.show_popup_window(title='О бэкапе методом синхронизации', text=text_2))
        text_3_1 = 'Программа проходит по исходному каталогу,\n'
        text_3_2 = 'и проверяет, что в конечном каталоге\nимеются те же файлы.\n'
        text_3_3 = 'Конечный каталог может содержать и другие файлы\n(но можно запустить проверку наоборот)'
        text_3 = text_3_1+text_3_2+text_3_3
        self.ui.action_Help_3.triggered.connect(lambda: self.show_popup_window(title='Об односторонней идентичности каталогов', text=text_3))
        #
        # объявление некоторых переменных
        funcs.variables_init(self)
        #
        # установка функциональности кнопок 
        self.ui.pushButton_1.clicked.connect(self.select_origin_directory)
        self.ui.pushButton_2.clicked.connect(self.select_synchr_directory)
        self.ui.pushButton_3.clicked.connect(self.compare_directories)
        self.ui.pushButton_4.clicked.connect(self.stop_scanning)
    #
    def show_popup_window(self, title, text):
        self.popup_window = QWidget()
        self.popup_window.setFixedSize(500, 200)
        self.popup_window.move(500, 300)
        self.popup_window.setWindowIcon(QIcon(funcs.resource_path('main_icon.ico')))
        self.popup_window.setWindowTitle(title)
        self.popup_window.label = QLabel(self.popup_window)
        self.popup_window.label.setGeometry(QtCore.QRect(20, 20, self.popup_window.width()-20*2, 120))
        self.popup_window.label.setFont(self.font_arial_16)
        self.popup_window.label.setText(text)
        self.popup_window.label.setAlignment(QtCore.Qt.AlignCenter)
        self.popup_window.pushButton = QPushButton(self.popup_window)
        self.popup_window.pushButton.setGeometry(QtCore.QRect(120, self.popup_window.height()-50, self.popup_window.width()-120*2, 30))
        self.popup_window.pushButton.setFont(self.font_arial_16)
        self.popup_window.pushButton.setText('OK')
        self.popup_window.pushButton.clicked.connect(self.popup_window.close)
        #
        self.popup_window.setStyleSheet("""
        QWidget {
            background-color: rgb(25, 35, 45); 
            color: rgb(255, 255, 191) 
        }
        QPushButton {
            background-color: rgb(240, 240, 240); 
            color: rgb(0, 0, 0)
        }
        QPushButton:hover {
            background-color: rgb(231, 255, 221); 
            color: rgb(0, 0, 0)
        }
        """)
        #
        self.popup_window.show()
    #
    def path_shortener(self, path, max_length=70): 
        if len(path) <= max_length: 
            return path 
        else: 
            a = max_length // 2 
            return path[0:a] + ' ... ' + path[-1-a:]
    #
    def select_origin_directory(self):
        if not self.scanning:
            try:
                self.origin_directory = QFileDialog.getExistingDirectory(self, 'Выберите исходный каталог')
                if self.origin_directory == '':
                    self.ui.pushButton_1.setText('исходный каталог: не выбран')
                else:
                    self.ui.pushButton_1.setText('исходный каталог: ' + self.path_shortener(self.origin_directory))
            except:
                self.ui.pushButton_1.setText('исходный каталог: не получилось выбрать') 
    #
    def select_synchr_directory(self):
        if not self.scanning:
            try:
                self.synchr_directory = QFileDialog.getExistingDirectory(self, 'Выберите синхронизированный каталог')
                if self.synchr_directory == '':
                    self.ui.pushButton_2.setText('синхронизированный каталог: не выбран')
                else:
                    self.ui.pushButton_2.setText('синхронизированный каталог: ' + self.path_shortener(self.synchr_directory))
            except:
                self.ui.pushButton_2.setText('синхронизированный каталог: не получилось выбрать')
    #
    def compare_directories(self): 
        #
        # Метод производит проверку корректности данных, и запускает сравнение каталогов self.origin_directory и self.synchr_directory
        #
        if not self.scanning:
            if self.origin_directory == '' or self.synchr_directory == '':
                self.show_popup_window('Ошибка: не выбран каталог',
                                       'Пожалуйста,\nвыберите\nисходный\nи синхронизированный\nкаталоги')
            elif self.synchr_directory == self.origin_directory:
                self.show_popup_window('Ошибка: выбран один и тот же каталог',
                                       'Пожалуйста,\nвыберите различающиеся\nисходный\nи синхронизированный\nкаталоги')
            else: 
                # старт проверки идентичности содержимого каталогов в отдельном потоке
                self.scanning = True
                self.ui.pushButton_1.setEnabled(False)
                self.ui.pushButton_2.setEnabled(False)
                self.ui.pushButton_3.setEnabled(False)
                self.ui.pushButton_4.setEnabled(True)
                self.make_compare_in_new_thread()
    #
    def make_compare_in_new_thread(self):
        #
        self.dt_stamp = date_time.now()
        self.ui.pushButton_3.setText(self.dt_stamp.nice_view + ': Проверка начата\nОтчёт записывается в файл log.txt')
        #
        self.compare_in_new_thread = Thread(target=funcs.make_compare, args=(self, ), daemon=True)
        self.compare_in_new_thread.start()
    #
    def stop_scanning(self):
        #
        if self.scanning:
            #
            self.scanning = False
            #
            funcs.variables_init(self)
            funcs.stop_scanning_buttons_and_labels_set_properties(self)


CSS_list = '''
QMenuBar {
    color: rgb(255, 255, 191) 
}
QMenu {
    color: rgb(255, 255, 191) 
}
'''


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.move(300, 100)
    #
    app.setStyleSheet(CSS_list)
    #
    main_window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
