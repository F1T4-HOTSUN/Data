from datetime import datetime
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from pickle import *
from pandas import json_normalize


class HolCaller:
    def __init__(self):
        data = {}
        with open("secret_data.pickle", "rb") as sd:
            data = load(sd)
        self.service_key = data.get("hol_service_key")

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

        # list = [id.string for id in xmlobj.find_all("locdate")]
        l = list(map(lambda x: x.string[:4] + '-' + x.string[4:6] + '-' + x.string[6:8], xmlobj.find_all("locdate")))

        return l

