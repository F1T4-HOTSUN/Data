from fclty_tools import *
from fclty_api_caller import FcltyCaller
from fclty_dao import *
from hol_api_caller import HolCaller
from prf_api_caller import *
from prf_dao import *
from prf_session_data import *
from datetime import datetime

fclty_new_list = FcltyCaller().get_id_list(10000)
old_list = FcltyDAO().select_id_list()
added_facilities = ListCheck().get_added_list(fclty_new_list, old_list)

fclty_data = []
for id in added_facilities:
    fclty_data.append(FcltyCaller().get_facility(id))

FcltyDAO().insert_data(fclty_data)


prf_new_list = PrfCaller().get_id_list(100, '01')
prf_new_list.extend(PrfCaller().get_id_list(100, '02'))
old_list = PrfDAO().select_prf_id_list()
added_performances = ListCheck().get_added_list(prf_new_list, old_list)


prf_data = []
for id in added_performances:
    getData = PrfCaller().get_performance(id)
    if getData != None:
        prf_data.append(getData)

hol_list = HolCaller().get_holiday(datetime.now().year)
hol_list += HolCaller().get_holiday(datetime.now().year+1)

session_list = []
for prf in prf_data:
    session_list += Session().session_data(prf['performance_id'], prf['dtguidance'], prf['prf_start_date'], prf['prf_end_date'], hol_list)


PrfDAO().insert_prf_data(prf_data)
PrfDAO().insert_session_data(session_list)