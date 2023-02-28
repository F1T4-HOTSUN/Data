from fclty_tools import *
from fclty_api_caller import FcltyCaller
from fclty_dao import *

new_list = FcltyCaller().get_id_list(10000)
old_list = FcltyDAO().select_id_list()
added_facilities = ListCheck().get_added_list(new_list, old_list)

data = []
for id in added_facilities:
    data.append(FcltyCaller().get_facility(id))

FcltyDAO().insert_data(data)
