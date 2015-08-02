import json
import requests
from bs4 import BeautifulSoup

city_code_name_pairs = {
    '1100': '서울특별시',
    '2600': '부산광역시',
    '2700': '대구광역시',
    '2800': '인천광역시',
    '2900': '광주광역시',
    '3000': '대전광역시',
    '3100': '울산광역시',
    '5100': '세종특별자치시',
    '4100': '경기도',
    '4200': '강원도',
    '4300': '충청북도',
    '4400': '충청남도',
    '4500': '전라북도',
    '4600': '전라남도',
    '4700': '경상북도',
    '4800': '경상남도',
    '4900': '제주특별자치도'
}


def fetch_election_district_info(city_code):
    url = ('http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?'
           'electionId=0020120411&requestURI=%%2Felectioninfo%%2F0020120411%%2Fbi%%2Fbigi05.jsp'
           '&statementId=BIGI05&electionCode=2&cityCode=%d&townCode=-1') % city_code
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')

    district_list = []
    last_district_name = None
    for tr in trs:
        tds = tr.find_all('td')
        associated_towns = [x.strip() for x in tds[2].string.split(',')]
        district_name = tds[0].string
        if district_name is None:
            district_name = last_district_name
        local_name = tds[1].string

        last_district_name = district_name
        precint_info = {
            'name': district_name,
            'local': local_name,
            'associated_towns': associated_towns
        }
        district_list.append(precint_info)
    return district_list


def fetch_all_city_district_infos():
    city_infos = []
    for k, v in city_code_name_pairs.items():
        city_info = {
            'code': k,
            'name': v,
            'district_info': fetch_election_district_info(int(k))
        }
        city_infos.append(city_info)
    return city_infos

if __name__ == '__main__':
    data_json = json.dumps(fetch_all_city_district_infos(), ensure_ascii=False)
    with open('election-data.json', 'w', encoding='utf-8') as f:
        f.write(data_json)
