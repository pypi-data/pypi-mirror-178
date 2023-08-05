import json


def convert_data(self, QMessageBox):

    try:
        with open(self.save_json_file) as train_data:
            train = json.load(train_data)

        train_ = []
        test_data = []
        for data in train:
            try:
                ents = [tuple(entity) for entity in data["entities"]]
                test_data.append((data["content"], {"entities": ents}))
                with open("{}".format("test.txt"), "w", encoding="utf-8") as write:
                    write.write(str(test_data))
                train_.append((data["content"], {"entities": ents}))
            except:
                test_data = []
                pass
        with open(
            "{}".format(self.txt_fldr + "/" + self.json_file.replace("json", "txt")),
            "w",
            encoding="utf-8",
        ) as write:
            write.write(str(train_))
        QMessageBox.about(self, "Message", "Annotation data saved in txt format")
    except:
        pass
