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

# fclty_new_list = FcltyCaller().get_id_list(100)
# old_list = FcltyDAO().select_id_list()
# added_facilities = ListCheck().get_added_list(fclty_new_list, old_list)

fclty_new_list = set()  # 새로운 시설 ID를 저장할 집합 (중복 방지)
old_list = set(FcltyDAO().select_id_list())  # 기존 ID 리스트를 집합으로 변환

# 반복하여 데이터 수집
for i in range(2, 33):
    new_ids = set(FcltyCaller().get_id_list(100, i))  # i 값을 추가하여 get_id_list 호출
    fclty_new_list.update(new_ids)  # 새로운 데이터를 누적하여 추가

# old_list와 비교하여 추가된 시설 ID 리스트를 생성
added_facilities = ListCheck().get_added_list(list(fclty_new_list), list(old_list))

fclty_data = []
for id in added_facilities:
    fclty_data.append(FcltyCaller().get_facility(id))

FcltyDAO().insert_data(fclty_data)

prf_new_list = PrfCaller().get_id_list(100, '02', 1)
prf_new_list.extend(PrfCaller().get_id_list(100, '02', 2))
prf_new_list.extend(PrfCaller().get_id_list(100, '02', 3))
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

