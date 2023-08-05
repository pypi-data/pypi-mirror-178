def json_formate(self, content, result_list):
    entities = []
    # self.not_empy=False
    if content[2] != [0, 0]:
        entities = [
            [macthing_content[2][0], macthing_content[2][1], macthing_content[1]]
            for macthing_content in result_list
            if macthing_content[2] != [0, 0] and macthing_content[3] == content[3]
        ]
        json_file = {  # merge all entites with single content
            "content": content[3],  # single content
            "entities": entities,  # and it's entities list
        }
        return json_file
    else:
        json_file = {  # merge all entites with single content
            "content": content[3],  # single content
            "entities": [[0, 0, self.selected_entity]],  # and it's entities list
        }
        return json_file
