import os, sys
from hashlib import md5
from PyQt5.QtGui import QIcon, QPixmap, QFont
from classes import date_time


def resource_path(relative_path, in_catalog='icons'):
    #
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.getcwd(), in_catalog))
    #
    return os.path.join(base_path, relative_path)


def get_md5sum(filepath):
    #
    md5_hash = md5()
    #
    with open(filepath, 'rb') as file:
        for part in iter(lambda: file.read(128*md5_hash.block_size), b''):
            md5_hash.update(part)
    #
    return md5_hash.hexdigest()


def set_window_sizes(obj):
    obj.width_origin = obj.width(); obj.height_origin = obj.height()
    obj.setMinimumSize(obj.width_origin, obj.height_origin)
    obj.resized.connect(lambda: ui_modification_in_case_resized(obj))
    #
    return 0


def ui_modification_in_case_resized(obj):
    #
    new_width = obj.width(); new_height = obj.height()
    delta_x = new_width-obj.width_origin; delta_y = new_height-obj.height_origin
    #
    obj.ui.label_2.move(110 + delta_x//2, 20)
    obj.ui.label_3.move(110 + delta_x // 2, 60)
    #
    obj.ui.pushButton_1.resize(840 + delta_x, 40)
    obj.ui.pushButton_2.resize(840 + delta_x, 40)
    obj.ui.pushButton_3.resize(640 + delta_x//2, 50)
    obj.ui.pushButton_4.move(690 + delta_x//2, 240)
    obj.ui.pushButton_4.resize(180 + delta_x//2, 50)
    #
    obj.ui.label_4.resize(840 + delta_x, 60)
    #
    return 0


def set_main_ico_and_title(obj):
    #
    obj.setWindowIcon(QIcon(resource_path('main_icon.ico')))
    obj.ui.label_1.setPixmap(QPixmap(resource_path('logo.png')))
    obj.setWindowTitle('Программа контроля бэкапов, сделанных методом синхронизации')
    #
    return 0


def set_fonts(obj):
    #
    obj.font_courier_16_bold = QFont('Courier'); obj.font_courier_16_bold.setPixelSize(16); obj.font_courier_16_bold.setBold(True)
    obj.font_courier_24_bold = QFont('Courier'); obj.font_courier_24_bold.setPixelSize(24); obj.font_courier_24_bold.setBold(True)
    obj.font_arial_16 = QFont('Arial'); obj.font_arial_16.setPixelSize(16); obj.font_arial_16.setBold(False)
    #
    obj.ui.label_2.setFont(obj.font_courier_24_bold)
    obj.ui.label_3.setFont(obj.font_courier_16_bold)
    #
    obj.ui.pushButton_1.setFont(obj.font_arial_16)
    obj.ui.pushButton_2.setFont(obj.font_arial_16)
    obj.ui.pushButton_3.setFont(obj.font_arial_16)
    obj.ui.pushButton_4.setFont(obj.font_arial_16)
    #
    return 0


def set_menu_icons(obj):
    #
    obj.ui.action_File_1.setIcon(QIcon(resource_path('catalog_icon.png')))
    obj.ui.action_File_1.setShortcut('Ctrl+O')
    obj.ui.action_File_2.setIcon(QIcon(resource_path('catalog_icon.png')))
    obj.ui.action_File_2.setShortcut('Ctrl+S')
    obj.ui.action_File_3.setIcon(QIcon(resource_path('check_icon.png')))
    obj.ui.action_File_3.setShortcut('Ctrl+C')
    obj.ui.action_File_4.setIcon(QIcon(resource_path('quit_icon.png')))
    obj.ui.action_File_4.setShortcut('Ctrl+Q')
    #
    obj.ui.action_Help_1.setIcon(QIcon(resource_path('info_icon.png')))
    obj.ui.action_Help_2.setIcon(QIcon(resource_path('info_icon.png')))
    obj.ui.action_Help_3.setIcon(QIcon(resource_path('info_icon.png')))
    #
    return 0


def set_buttons_hover_properties(obj):
    #
    # Функция осуществляет установку цвета некоторых кнопок при наведении на них указателя мыши
    #
    color_code = '#E7FFDD'
    #
    for i in range(1, 4+1):
        getattr(obj.ui, 'pushButton_{}'.format(i)).setStyleSheet("""
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
    return 0


def size_transform(size):
    if size > 1024**3:
        return (round(size/1024**3, 2), 'ГБ')
    elif size > 1024**2:
        return (round(size/1024**2, 2), 'МБ')
    elif size > 1024:
        return (round(size/1024, 2), 'кБ')
    else:
        return (size, 'Б')


def variables_init(obj):
    obj.origin_directory = ''
    obj.synchr_directory = ''
    obj.scanning = False
    obj.synchr_err = 0
    obj.file_number = 0
    obj.size_total = 0


def stop_scanning_buttons_and_labels_set_properties(obj):
    #
    obj.ui.pushButton_1.setText('исходный каталог')
    obj.ui.pushButton_2.setText('синхронизированный каталог')
    obj.ui.pushButton_3.setText('Проверить идентичность содержимого каталогов\nи записать результат в лог (.txt)')
    #
    obj.ui.pushButton_1.setEnabled(True)
    obj.ui.pushButton_2.setEnabled(True)
    obj.ui.pushButton_3.setEnabled(True)
    obj.ui.pushButton_4.setEnabled(False)


def make_compare(obj, recursion_level=1, current_origin_directory='', current_synchr_directory='', log_filename='log.txt'):
    #
    # Функция реализует рекурсивный обход файлов в каталоге obj.origin_directory и его подкаталогах,
    # ищет такие же файлы в каталоге obj.synchr_directory и его таких же подкаталогах,
    # одновременно производя для всех файлов вычисления md5sum, попарное сравнение вычисленных md5sum, и запись информации в log.txt
    #
    if obj.scanning and recursion_level == 1:
        #
        with open(os.path.join(os.getcwd(), log_filename), 'a') as file_report:
            dt_stamp = date_time.now()
            file_report.write('\n' + dt_stamp.nice_view + ' - Проверка начата\n')
        current_origin_directory = obj.origin_directory
        current_synchr_directory = obj.synchr_directory
    #
    for name in os.listdir(current_origin_directory):
        #
        if obj.scanning:
        #
            path_to_item = os.path.join(current_origin_directory, name)
            #
            if os.path.isfile(path_to_item):
                #
                if True: #try:
                    file_size = os.path.getsize(path_to_item)
                    #
                    filehash_origin = get_md5sum(path_to_item)
                    filehash_synchr = get_md5sum(os.path.join(current_synchr_directory, name))
                    #
                    if filehash_synchr != filehash_origin:
                        text_pattern = 'Хеш файла {} не совпадает с хешем синхрофайла,\nадрес: {}\n\n'
                        with open(os.path.join(os.getcwd(), log_filename), 'a') as file_report:
                            dt_stamp = date_time.now()
                            file_report.write('\n' + dt_stamp.nice_view + ' - ' + text_pattern.format(name, path_to_item))
                        obj.synchr_err += 1
                    #
                    obj.file_number += 1
                    obj.size_total += file_size
                    text_pattern = 'Проверен файл {} размером {} {}\n\nВсего проверено {} файлов размером {} {}'
                    text_info = text_pattern.format(name, *size_transform(file_size), obj.file_number, *size_transform(obj.size_total))
                    obj.ui.label_4.setText(text_info)
                #
                else: # except:
                    text_pattern = 'Не удалось проверить файл {} в исходном или синхронизируемом каталоге,\nадрес: {}\n\n'
                    with open(os.path.join(os.getcwd(), log_filename), 'a') as file_report:
                        dt_stamp = date_time.now()
                        file_report.write('\n' + dt_stamp.nice_view + ' - ' + text_pattern.format(name, path_to_item))
                    obj.synchr_err += 1
            #
            elif os.path.isdir(path_to_item):
                make_compare(obj, recursion_level=recursion_level+1, current_origin_directory=path_to_item,
                             current_synchr_directory=os.path.join(current_synchr_directory, name))
        #
        else:
            #
            obj.ui.label_4.setText('')
            #
            if recursion_level == 1:
                text_pattern = 'Проверка была остановлена.\n\n'
                with open(os.path.join(os.getcwd(), log_filename), 'a') as file_report:
                    dt_stamp = date_time.now()
                    file_report.write('\n' + dt_stamp.nice_view + ' - ' + text_pattern)
            #
            break
    #
    if obj.scanning and recursion_level == 1:
        #
        if not obj.synchr_err:
            text_pattern = 'Проверено файлов: {}. Содержимое каталогов (как минимум односторонне) идентично.'.format(obj.file_number)
        else:
            #
            text_pattern = 'Проверено файлов: {}. Содержимое каталогов неидентично, ошибок: {}.'.format(obj.file_number, obj.synchr_err)
        #
        dt_stamp = date_time.now()
        #
        with open(os.path.join(os.getcwd(), log_filename), 'a') as file_report:
            file_report.write(dt_stamp.nice_view + ' - ' + text_pattern + '\n\n\n')
        #
        obj.ui.label_4.setText(dt_stamp.nice_view + ' - ' + text_pattern)
        #
        variables_init(obj)
        stop_scanning_buttons_and_labels_set_properties(obj)
    #
    return 0


