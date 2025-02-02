import os

from fclty_tools import *
import requests
from bs4 import BeautifulSoup


class FcltyCaller:
    def __init__(self):
        data = {}
        self.service_key = os.environ['KOPIS_SERVICE_KEY']

    def get_id_list(self, row, page):
        url = "http://www.kopis.or.kr/openApi/restful/prfplc"
        params = {
            'service': self.service_key,
            'cpage': page,
            'rows': row
        }
        response = requests.get(url, params=params).text

        xmlobj = BeautifulSoup(response, 'lxml-xml')

        list = [id.string for id in xmlobj.find_all("mt10id")]

        return list

    def get_facility(self, fclty_id):
        url = "http://www.kopis.or.kr/openApi/restful/prfplc/{0}".format(
            fclty_id)
        params = {
            'service': self.service_key,
            'mt10id': fclty_id
        }

        response = requests.get(url, params=params).text
        xmlobj = BeautifulSoup(response, 'lxml-xml').find("db")
        data = {}
        data["facility_id"] = xmlobj.find("mt10id").string
        data["facility_name"] = xmlobj.find("fcltynm").string
        data["facility_telno"] = Validation().check_none(
            xmlobj.find("telno").string)
        data["facility_relateurl"] = Validation().check_none(
            xmlobj.find("relateurl").string)
        data["facility_address"] = xmlobj.find("adres").string
        data["facility_latitude"] = float(xmlobj.find("la").string)
        data["facility_longitude"] = float(xmlobj.find("lo").string)

        return data
