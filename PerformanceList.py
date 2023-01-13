import requests
import bs4

def pef_id_list():
    serviceKey = "5d8e9c530c12433397b94fc06931bed2"
    stdate = "20230113"
    eddate = "20250101"

    url = "http://kopis.or.kr/openApi/restful/pblprfr"
    params={
        'service': serviceKey,
        'stdate': stdate,
        'eddate': eddate,
        'cpage': 1,
        'rows': 10000
    }

    # request요청 - xml 응답
    response = requests.get(url, params=params).text

    # bs4를 이용해 xml 파싱 후 xmlobject에 저장
    xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')

    # 공연id에 대한 값만 저장
    rows = xmlobj.findAll('mt20id')

    # 태그 제거
    performance_id = list(map(lambda x: x.string, rows))

    return performance_id