from fclty_tools import *
from fclty_api_caller import FcltyCaller
from fclty_dao import *
from hol_api_caller import HolCaller
from rank_dao import RankDAO
from rank_api_caller import RankCaller
from prf_api_caller import *
from prf_dao import *
from prf_session_data import *
from datetime import datetime
from pytz import timezone
import logging


logger = logging.getLogger()
logger.setLevel("DEBUG")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

fclty_new_list = FcltyCaller().get_id_list(10000)
old_list = FcltyDAO().select_id_list()
added_facilities = ListCheck().get_added_list(fclty_new_list, old_list)

fclty_data = []
for id in added_facilities:
    fclty_data.append(FcltyCaller().get_facility(id))

FcltyDAO().insert_data(fclty_data)-

prf_new_list = PrfCaller().get_id_list(5000, '01')
prf_new_list.extend(PrfCaller().get_id_list(1000, '02'))
old_list = PrfDAO().select_prf_id_list()
added_performances = ListCheck().get_added_list(prf_new_list, old_list)


prf_data = []
for id in added_performances:
    getData = PrfCaller().get_performance(id)
    if getData != None:
        prf_data.append(getData)

hol_list = HolCaller().get_holiday(datetime.now(timezone('Asia/Seoul')).year)
hol_list += HolCaller().get_holiday(datetime.now(timezone('Asia/Seoul')).year+1)

session_list = []
for prf in prf_data:
    session_list += Session().session_data(prf['performance_id'], prf['dtguidance'], prf['prf_start_date'], prf['prf_end_date'], hol_list)

PrfDAO().insert_prf_data(prf_data)
PrfDAO().insert_session_data(session_list)

rank_data = RankCaller().get_rank()
RankDAO().delete_rank_data()
RankDAO().insert_rank_data(rank_data)

