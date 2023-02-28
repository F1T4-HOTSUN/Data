import json
import xmltodict


class ListCheck:
    def __init__(self):
        pass

    def get_added_list(self, new_list, old_list):
        return set(new_list) - set(old_list)


class Validation:
    def __init__(self):
        pass

    def check_none(self, content):
        return content if content != ' ' or content != '' else None


class ParseToJson:
    def __init__(self):
        pass

    def xml_to_json(self, xml_str):
        if (Validation().check_none(xml_str) == None):
            return None
        if (Validation().check_none(xml_str) == 'None'):
            return None
        return json.dumps(xmltodict.parse(xml_str), indent=4, ensure_ascii=False)


class ParseToList:
    def __init__(self):
        pass

    def xml_to_list(self, xml_str):
        return list(map(lambda x: x.string, xml_str))

# class ParseToTable:
#     def __init__(self):
#         pass

#     def prepareSession(self, dtguidance):
