from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5 import QtCore

from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QPushButton
import os


def delete_from_entity(self, result_list, QApplication):
    # try:
    global entity_color_list
    button = QApplication.focusWidget()
    index = self.result_view.indexAt(button.pos())
    if index.isValid():
        self.clean = True
        cursor = self.edit.textCursor()
        if result_list[index.row()][2] != [] and self.save.text() != "Save":
            start = result_list[index.row()][2][0]
            end = result_list[index.row()][2][1]
            cursor.setPosition(start)
            cursor.movePosition(
                QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end - start
            )
            charfmt = cursor.charFormat()
            charfmt.setBackground(QColor(Qt.white))
            cursor.setCharFormat(charfmt)
            cursor.clearSelection()
            self.edit.setTextCursor(cursor)
        del result_list[index.row()]
        if len(result_list) == 0:
            self.result_view.setRowCount(len(result_list))
            self.save_json = True
        self.delet_ = True
        self.add_annotation_data()


# except:
#    pass
def add_entity_to_table(self, entity_list):
    # global path
    # (__file__, "../..")
    path = os.path.join(os.path.abspath(os.path.join(__file__, "../..")), "gui")
    # print("add", self.path)
    # path = os.path.dirname(os.path.abspath(__file__, "../.."))
    # print(path)
    # try:
    self.entity_view.setColumnCount(2)
    header = self.entity_view.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    self.entity_view.setHorizontalHeaderLabels(["Entity", "Option"])
    self.entity_view.setRowCount(len(entity_list))
    ii = 0
    for jj, entity in enumerate(entity_list):
        [R, G, B] = entity[1]
        item1 = QTableWidgetItem(str(entity[0]))
        item1.setBackground(QColor(R, G, B))
        self.entity_view.setItem(ii, 0, item1)
        self.delete_added_entity = QPushButton()
        self.delete_added_entity.setIcon(QIcon(QPixmap(path + "/Delete.png")))
        self.delete_added_entity.setIconSize(QtCore.QSize(30, 40))
        self.delete_added_entity.setStyleSheet(self.StyleSheet)
        self.delete_added_entity.clicked.connect(self.delete_entity)
        self.entity_view.setCellWidget(ii, 1, self.delete_added_entity)
        ii += 1


# except:
#    pass
