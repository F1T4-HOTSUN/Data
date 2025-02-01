import os

from fclty_tools import *
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone

class RankCaller:
    def __init__(self):
        self.service_key = os.environ['KOPIS_SERVICE_KEY']

    def get_rank(self):
        yesterday = (datetime.now(timezone('Asia/Seoul')).date() - timedelta(1)).strftime("%Y%m%d")
        url = "http://kopis.or.kr/openApi/restful/boxoffice"
        params = {
            'service': self.service_key,
            'stdate': yesterday,
            #'ststype': 'day',
            'eddate': yesterday,
            'date': yesterday
        }

        response = requests.get(url, params=params).text
        xmlobj = BeautifulSoup(response, 'lxml-xml').find_all("boxof")
        list = []
        for i in range(0, 10):
            data = {}
            data['performance_id'] = xmlobj[i].find("mt20id").string
            data['rnum'] = xmlobj[i].find("rnum").string
            data['basedate'] = yesterday
            list.append(data)

        return list






