def refresh(self):
    try:
        """
        it refresh application for new contents
        """
        global result_list
        result_list = []
        self.content_list = []
        self.selected_entity = ""
        self.clean = False
        self.save_json = False
        self.edit.setReadOnly(False)
        self.save.setText("Save")
        self.edit.setText("")
        self.result.setText("")
        while self.result_view.rowCount() > 0:
            self.result_view.removeRow(0)
    except:
        pass
