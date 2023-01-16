import json
import datetime
from pickle import *
import xmltodict
from bs4 import BeautifulSoup
import requests
from prf_tools import *


class PrfCaller:
    def __init__(self):
        data = {}
        with open("secret_data.pickle", "rb") as sd:
            data = load(sd)
        self.service_key = data.get("service_key")

    def get_id_list(self, row, prfstate):
        url = "http://kopis.or.kr/openApi/restful/pblprfr"
        params = {
            'service': self.service_key,
            'cpage': 1,
            'rows': row,
            'prfstate': prfstate
        }
        response = requests.get(url, params=params).text

        xmlobj = BeautifulSoup(response, 'lxml-xml')

        list = [id.string for id in xmlobj.find_all("mt20id")]

        return list

    def get_performance(self, prf_id):
        url = "http://kopis.or.kr/openApi/restful/pblprfr/{0}".format(prf_id)
        params = {
            'service': self.service_key
        }

        response = requests.get(url, params=params).text
        xmlobj = BeautifulSoup(response, 'lxml-xml').find("db")

        data = {}
        data["performance_id"] = xmlobj.find("mt20id").string
        data["facility_id"] = xmlobj.find("mt10id").string
        data["prf_title"] = xmlobj.find("prfnm").string
        data["prf_start_date"] = xmlobj.find(
            "prfpdfrom").string.replace('.', '-')
        data["prf_end_date"] = Validation().check_none(
            xmlobj.find("prfpdto").string.replace('.', '-'))
        data["prf_cast"] = Validation().check_none(
            xmlobj.find("prfcast").string)
        data["prf_crew"] = Validation().check_none(
            xmlobj.find("prfcrew").string)
        data["prf_runtime"] = xmlobj.find("prfruntime").string
        data["prf_prd_comp"] = Validation().check_none(
            xmlobj.find("entrpsnm").string)
        data["prf_viewing_age"] = xmlobj.find("prfage").string
        data["prf_ticket_price"] = xmlobj.find("pcseguidance").string
        data["prf_poster"] = Validation().check_none(
            xmlobj.find("poster").string)
        data["prf_story"] = Validation(
        ).check_none(xmlobj.find("sty").string)
        data["prf_genre"] = xmlobj.find("genrenm").string
        data["prf_openrun"] = xmlobj.find("openrun").string
        data["prf_styurls"] = ParseToJson().xml_to_json(
            str(xmlobj.find("styurls")).replace("\n", ""))
        data["prf_state"] = xmlobj.find("prfstate").string
        data["prf_loaded_at"] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')

        return data
