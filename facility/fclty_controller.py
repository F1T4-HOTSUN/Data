from fclty_api_caller import FcltyCaller
from fclty_dao import *
from fclty_tools import *

new_list = FcltyCaller().get_id_list(20)
old_list = FcltyDBController().select_id_list()
added_facilities = FacilityCheck().get_added_facilities(new_list, old_list)

data = []
for id in added_facilities:
    data.append(FcltyCaller().get_facility(id))

FcltyDBController().insert_data(data)
