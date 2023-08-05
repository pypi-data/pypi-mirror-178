from . import convert_to_json
import json


def save_to_json(self, result_list):
    # try:
    """
    save data in json file
    """
    if (
        self.save.text() != "Save" or self.delet_
    ):  # self.delet_==True mean if user delete entitie form list then algorithm update json file
        self.delet_ = False

        if (
            result_list != [] or self.save_json
        ):  # self.save_json==True mean if user delete all entitie form list then algorithm update json file
            self.save_json = False
            data = [
                convert_to_json.json_formate(self, content, result_list)
                for content in result_list
            ]
            remove_duplicate = [
                data[i] for i in range(len(data)) if data[i] not in data[i + 1 :]
            ]
            json_form = json.dumps(remove_duplicate)  # convert to json format
            self.result.setText("")
            self.result.append(json_form)  # show to user in textbox
            with open(self.save_json_file, "w") as content:  # save file
                content.write(json_form)


# except:
#     pass
