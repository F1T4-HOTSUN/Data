import datetime
import os
from bs4 import BeautifulSoup
import requests
from prf_tools import *
from datetime import datetime, timedelta
from pytz import timezone


class PrfCaller:
    def __init__(self):
        data = {}
        self.service_key = os.environ['KOPIS_SERVICE_KEY']

    def get_id_list(self, row, prfstate, page):
        yesterday = (datetime.now(timezone('Asia/Seoul')).date() - timedelta(1)).strftime("%Y%m%d")
        url = "http://kopis.or.kr/openApi/restful/pblprfr"
        params = {
            'service': self.service_key,
            'cpage': page,
            'rows': row,
            #'prfstate': prfstate,
            # 데이터가 최대한 필요해서 임시로 날짜 넣음
            #'eddate': yesterday,
            #'stdate': yesterday
            'eddate': yesterday,
            'stdate': '20100101'
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

        dtguidance = xmlobj.find("dtguidance").string
        if dtguidance == ' ' or dtguidance == '':
            return None

        prf_ticket_price = xmlobj.find("pcseguidance").string
        if prf_ticket_price == ' ' or prf_ticket_price == '':
            return None

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
        data["prf_runtime"] = Validation().check_none(
            xmlobj.find("prfruntime").string)
        data["prf_prd_comp"] = Validation().check_none(
            xmlobj.find("entrpsnm").string)
        data["prf_viewing_age"] = xmlobj.find("prfage").string
        data["prf_ticket_price"] = Validation().check_none(
            xmlobj.find("pcseguidance").string)
        data["prf_poster"] = Validation().check_none(
            xmlobj.find("poster").string)
        data["prf_story"] = Validation(
        ).check_none(xmlobj.find("sty").string)
        data["prf_genre"] = xmlobj.find("genrenm").string
        data["prf_openrun"] = xmlobj.find("openrun").string
        data["prf_styurls"] = Validation().check_none(
            str(ParseToList().xml_to_list(xmlobj.findAll("styurl"))).replace("\'", "").replace("[","").replace("]","") )
        data["prf_state"] = xmlobj.find("prfstate").string
        data["prf_loaded_at"] = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')
        data["dtguidance"] = xmlobj.find("dtguidance").string

        return data
