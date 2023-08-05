from . import save_in_json_format
from PyQt5.QtGui import *
from PyQt5.Qt import Qt


def next_new_content(self, result_list, QMessageBox):
    # try:
    # global result_list
    if self.edit.toPlainText() != "":
        if self.selected_entity != "":
            if self.save.text() != "Save":
                text = self.edit.toPlainText()

                if len(result_list) > 0:
                    check = [chck for chck in result_list if chck[3] == text]
                    if not check:
                        try:
                            result_list.append(
                                [
                                    "",
                                    self.selected_entity,
                                    [0, 0],
                                    text,
                                    [100, 100, 100],
                                ]
                            )
                            self.add_annotation_data()
                            save_in_json_format.save_to_json(self, result_list)
                        except:
                            pass
                else:

                    result_list.append(
                        ["", self.selected_entity, [0, 0], text, [100, 100, 100]]
                    )
                    self.add_btn = True
                    self.add_annotation_data()
                    save_in_json_format.save_to_json(self, result_list)
                self.edit.setText("")
                cursor = self.edit.textCursor()
                charfmt = cursor.charFormat()
                charfmt.setBackground(QColor(Qt.white))
                cursor.setCharFormat(charfmt)
                cursor.clearSelection()
                self.edit.setTextCursor(cursor)
                self.save.setText("Save")
                self.edit.setReadOnly(False)

            else:
                QMessageBox.about(
                    self, "Message", "first save content, click on save button"
                )
        else:
            QMessageBox.about(self, "Message", "select entity from left side table")


# except:
#    pass
