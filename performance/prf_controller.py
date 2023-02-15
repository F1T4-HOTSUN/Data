from performance.hol_api_caller import HolCaller
from prf_api_caller import *
from prf_dao import *
from prf_session_data import *

new_list = PrfCaller().get_id_list(10000, "01")
old_list = PrfDAO().select_prf_id_list()
added_performances = ListCheck().get_added_list(new_list, old_list)


data = []
for id in added_performances:
    data.append(PrfCaller().get_performance(id))


hol_list = HolCaller().get_holiday(datetime.now().year)
hol_list += HolCaller().get_holiday(datetime.now().year+1)

session_list = []
for prf in data:
    session_list += Session().session_data(prf['performance_id'], prf['dtguidance'], prf['prf_start_date'], prf['prf_end_date'], hol_list)


PrfDAO().insert_prf_data(data)
PrfDAO().insert_session_data(session_list)
