from prf_tools import *
from prf_api_caller import *
from prf_dao import *
import datetime


new_list = PrfCaller().get_id_list(3, "01")
old_list = PrfDAO().select_prf_id_list()
added_performances = ListCheck().get_added_list(new_list, old_list)


data = []
for id in added_performances:
    data.append(PrfCaller().get_performance(id))

print(data)

# print(data)
PrfDAO().insert_prf_data(data)
