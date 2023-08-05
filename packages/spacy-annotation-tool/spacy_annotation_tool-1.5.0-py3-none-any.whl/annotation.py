from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QTextEdit,
    QApplication,
    QMessageBox,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.Qt import Qt
import pandas as pd
import json

# from PyQt5.QtWidgets import QTextEdit,QWidget,QVBoxLayout,QApplication,QWidget,QRubberBand
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys
import os
import re
from packages import style_sheet
from packages import convert_json_to_txt, refresh_clean, save_in_json_format
from packages import next_content
from packages import table_view

import os

# global path
# path = os.path.dirname(os.path.abspath(__file__))
# print(path)


class MainPageWindo(QMainWindow):
    def __init__(self):
        # global path
        self.path = os.path.dirname(os.path.abspath(__file__))
        super().__init__()
        loadUi(self.path + "/design/annotation.ui", self)
        global entity_color_list, result_list
        self.json_fldr = "json_format"
        self.txt_fldr = "txt_format"
        try:
            os.mkdir(self.json_fldr)
            self.json_file = "contents.json"
            self.save_json_file = self.json_fldr + "/" + self.json_file
        except:
            path, dirs, files = next(os.walk(self.json_fldr))
            total = len(files)
            self.json_file = "contents" + str(total) + ".json"
            self.save_json_file = self.json_fldr + "/" + self.json_file

        try:
            os.mkdir(self.txt_fldr)
        except:
            pass
        self.setWindowTitle("Expert Annotation ")
        self.content_list = []
        self.selected_entity = ""  # select entity from
        self.clean = False
        self.save_json = False
        self.add_btn = False
        # self.empty=True
        self.delet_ = False
        self.StyleSheet = style_sheet.design()
        entity_color_list = []
        result_list = []
        self.crop = ""
        self.start = 0
        self.end = 0
        self.edit.selectionChanged.connect(self.text_selection_changed)
        self.save.clicked.connect(self.save_text)
        self.add.clicked.connect(self.add_annotation_data)
        self.add_entity.clicked.connect(self.new_entity)
        self.entity_view.cellClicked.connect(self.click_table)
        self.clear.clicked.connect(self.refresh)
        self.Next.clicked.connect(self.new_content)
        self.edit.installEventFilter(self)
        self.txt.clicked.connect(self.txt_data)
        self.save.setToolTip("Save Content")
        self.add.setToolTip("Add Entity")

    def new_content(self):
        global result_list
        next_content.next_new_content(self, result_list, QMessageBox)

    def txt_data(self):
        convert_json_to_txt.convert_data(self, QMessageBox)

    def check(self):
        global entity_color_list
        if len(entity_color_list) == 0:
            QMessageBox.about(
                self,
                "Message",
                "No entity found, add entity in right side table then select text",
            )
        elif self.selected_entity == "":
            QMessageBox.about(
                self,
                "Message",
                "First select entity from right side table just click on entity",
            )

    def refresh(self):
        refresh_clean.refresh(self)

    def eventFilter(self, widget, event):
        """
        if user not click on Edit button and user want to change in content then its prompt to user that click on edit button
        """
        if (
            event.type() == QtCore.QEvent.KeyPress
            and event.type() != QtCore.QEvent.Enter
            and widget is self.edit
            and self.save.text() == "Edit"
        ):
            QMessageBox.about(
                self,
                "Message",
                "Please click on edit button if you want to change the Content",
            )
        return QWidget.eventFilter(self, widget, event)

    def click_table(self):
        # try:
        global entity_color_list
        for ii, current_tabel_item in enumerate(self.entity_view.selectedItems()):
            self.row = current_tabel_item.row()
            self.selected_entity = current_tabel_item.text()
            self.color = [
                color[1]
                for color in entity_color_list
                if color[0] == self.selected_entity
            ][0]

    # except:
    #    pass

    def new_entity(self):
        # try:
        if self.entity.text() != "":
            global entity_color_list
            entity = self.entity.text()
            R = random.randint(0, 255)
            G = random.randint(0, 255)
            B = random.randint(0, 255)
            if G < 40:
                self.new_entity()
            condition = [single for single in entity_color_list if single[0] == entity]
            if condition == []:
                entity_color_list.append([entity, [R, G, B]])
                table_view.add_entity_to_table(self, entity_color_list)
            self.entity.setText("")
        else:
            QMessageBox.about(self, "Message", "Please add entity")

    # except:
    #    pass
    #
    def add_annotation_data(self):
        # global path
        path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), "gui")

        # path = path + "/gui/Delete.png"
        print(path)
        # try:
        if self.save.text() != "Save" or self.delet_:
            global result_list
            if self.add_btn:
                try:
                    if not self.clean:
                        # self.empty=False
                        word = self.text[self.start : self.end]
                        if word.startswith((" ", "\t")):
                            self.start = self.start + 1
                        if word.endswith((" ", "\t")):
                            self.end = -1
                        word = self.text[self.start : self.end]
                        if word != "":
                            list_ = [
                                word,
                                self.selected_entity,
                                [self.start, self.end],
                                self.text,
                                self.color,
                            ]
                            result_list.append(list_)
                            res = []
                            [res.append(x) for x in result_list if x not in res]
                            result_list.clear()
                            result_list = res
                        cursor = self.edit.textCursor()
                        start = self.start
                        end = self.end
                        cursor.setPosition(start)
                        cursor.movePosition(
                            QTextCursor.NextCharacter,
                            QTextCursor.KeepAnchor,
                            end - start,
                        )
                        charfmt = cursor.charFormat()
                        [R, G, B] = self.color
                        charfmt.setBackground(QtGui.QColor(R, G, B))
                        cursor.setCharFormat(charfmt)
                        cursor.clearSelection()
                        self.edit.setTextCursor(cursor)
                except Exception as e:
                    pass

                if len(result_list) != 0:
                    self.save_json = True
                self.result.setText("")
                self.result_view.setColumnCount(4)
                save_in_json_format.save_to_json(self, result_list)
                header = self.result_view.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.Stretch)
                header.setSectionResizeMode(1, QHeaderView.Stretch)
                header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
                self.result_view.setHorizontalHeaderLabels(
                    ["Entity", "Result", "Delete", "Edit"]
                )
                self.result_view.setRowCount(len(result_list))
                index = 0
                for entity in result_list:

                    result = entity[0]
                    label = entity[1]
                    [R, G, B] = entity[4]
                    result = QTableWidgetItem(str(result))
                    label = QTableWidgetItem(str(label))
                    label.setBackground(QtGui.QColor(R, G, B))
                    self.result_view.setItem(index, 0, label)
                    self.result_view.setItem(index, 1, result)

                    self.delete_annotated_ = QPushButton()
                    self.delete_annotated_.setIcon(QIcon(QPixmap(path + "/Delete.png")))
                    self.delete_annotated_.setIconSize(QtCore.QSize(30, 40))
                    self.delete_annotated_.setMaximumWidth(40)
                    self.delete_annotated_.setMaximumHeight(40)
                    self.delete_annotated_.setStyleSheet(self.StyleSheet)
                    self.delete_annotated_.clicked.connect(self.delete_annotated_entity)
                    self.edit_annotated_ = QPushButton()
                    self.edit_annotated_.setIcon(QIcon(QPixmap("edit.png")))
                    self.edit_annotated_.setIconSize(QtCore.QSize(30, 40))
                    self.edit_annotated_.setMaximumWidth(30)
                    self.edit_annotated_.setMaximumHeight(30)
                    self.edit_annotated_.setStyleSheet(self.StyleSheet)
                    self.edit_annotated_.clicked.connect(self.edit_content)
                    self.result_view.setCellWidget(index, 2, self.delete_annotated_)
                    self.result_view.setCellWidget(index, 3, self.edit_annotated_)
                    index += 1
        else:
            QMessageBox.about(
                self, "Message", "first save content, click on save button"
            )

    # except:
    #    pass

    def edit_content(self):
        global entity_color_list, result_list
        button = QApplication.focusWidget()
        index = self.result_view.indexAt(button.pos())
        if index.isValid():
            # self.clean=True
            # cursor = self.edit.textCursor()
            # if result_list[index.row()][2]!=[]:
            #     start=result_list[index.row()][2][0]
            #     end=result_list[index.row()][2][1]
            #     cursor.setPosition(start)
            #     cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end-start)
            #     charfmt = cursor.charFormat()
            #     charfmt.setBackground(QColor(Qt.white))
            #     cursor.setCharFormat(charfmt)
            #     cursor.clearSelection()
            #     self.edit.setTextCursor(cursor)
            self.edit.setText(result_list[index.row()][3])
            self.start = result_list[index.row()][2][0]
            self.end = result_list[index.row()][2][1]
            self.color = result_list[index.row()][4]
            word = self.text[self.start : self.end]
            if word != "":
                list_ = [
                    word,
                    self.selected_entity,
                    [self.start, self.end],
                    self.text,
                    self.color,
                ]
                result_list.append(list_)
                res = []
                [res.append(x) for x in result_list if x not in res]
                result_list.clear()
                result_list = res
            cursor = self.edit.textCursor()
            start = self.start
            end = self.end
            cursor.setPosition(start)
            cursor.movePosition(
                QTextCursor.NextCharacter, QTextCursor.KeepAnchor, end - start
            )
            charfmt = cursor.charFormat()
            [R, G, B] = self.color
            charfmt.setBackground(QtGui.QColor(R, G, B))
            cursor.setCharFormat(charfmt)
            cursor.clearSelection()
            self.edit.setTextCursor(cursor)
        #     if len(result_list)==0:
        #         self.result_view.setRowCount(len(result_list))
        #         self.save_json=True
        #     self.delet_=True
        #     self.add_annotation_data()

    def delete_annotated_entity(self):
        global result_list
        table_view.delete_from_entity(self, result_list, QApplication)

    def save_text(self):
        try:
            if self.save.text() == "Edit":
                self.edit.setReadOnly(False)
                self.save.setText("Save")
            elif self.save.text() == "Save":
                if self.edit.toPlainText() != "":

                    self.edit.setText(self.process_email(self.edit.toPlainText()))
                    self.edit.setReadOnly(True)
                    self.save.setText("Edit")
                    self.start = 0
                    self.end = 0
                    self.text = self.edit.toPlainText()
                    self.text = self.text.strip()
                    # self.text = self.process_email(self.text)
                    # self.empty=True
                else:
                    QMessageBox.about(
                        self, "Message", "Content not found, first write content"
                    )
        except:
            pass

    def process_email(self, email):
        email = re.sub("\u200b", "", email)
        email = re.sub("\|", ".", email)
        email = re.sub(":", ".", email)
        email = re.sub("stocks last", "stocks lasts", email)
        email = re.sub(
            "(facebook|twitter|youtube|pinterest|instagram|whatsapp|tiktok)",
            "",
            email,
            flags=re.IGNORECASE,
        )
        # email=re.sub('\n','. ',email)
        email = re.sub(r"[^a-zA-Z0-9%.:,()\'/\-+$€£!]", " ", email)
        email = re.sub(r"\.{3,}", "", email)
        email = re.sub(r"\s{3,}", " ", email)
        return email

    def delete_entity(self):
        # try:
        global entity_color_list
        button = QApplication.focusWidget()
        index = self.entity_view.indexAt(button.pos())
        if index.isValid():
            # print(entity_color_list.pop(index.row()))
            if self.selected_entity == entity_color_list.pop(index.row())[0]:
                self.selected_entity = ""
            # entity_color_list.pop(index.row())
            table_view.add_entity_to_table(self, entity_color_list)

    # except:
    #    pass

    def text_selection_changed(self):
        try:
            global entity_color_list
            if len(entity_color_list) == 0 or self.selected_entity == "":
                self.check()
            else:
                self.clean = False
                self.add_btn = True
                cursor = self.edit.textCursor()
                self.start = cursor.selectionStart()
                self.end = cursor.selectionEnd()
        except:
            pass


# if __name__ == "__main__":
app = QApplication(sys.argv)
widget = MainPageWindo()
widget.show()
sys.exit(app.exec_())
