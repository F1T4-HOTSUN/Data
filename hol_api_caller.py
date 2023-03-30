import os
import requests
from bs4 import BeautifulSoup

class HolCaller:
    def __init__(self):
        data = {}
        self.service_key = os.environ['HOL_SERVICE_KEY']

    def get_holiday(self, year):
        url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
        params = {
            'serviceKey': self.service_key,
            'pageNo': 1,
            'numOfRows': 1000,
            'solYear': year,
        }

        response = requests.get(url, params=params).text

        xmlobj = BeautifulSoup(response, 'lxml-xml')

        l = list(map(lambda x: x.string[:4] + '-' + x.string[4:6] + '-' + x.string[6:8], xmlobj.find_all("locdate")))

        return l

