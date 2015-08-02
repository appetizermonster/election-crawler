import json

district_data = json.load(open('election-data.json', 'r', encoding='utf-8'))
assembly_data = json.load(open('assembly.json', 'r', encoding='utf-8'))


def find_district_name(city_name, local_name, town_name):
    city_info = list(
        filter(lambda x: x['name'] == city_name, district_data))[0]
    district_info = city_info['district_info']
    district_candiates = list(
        filter(lambda x: x['local'] == local_name, district_info))
    selected_district_info = None
    for district_info in district_candiates:
        is_town_exists = district_info['associated_towns'].index(town_name)
        if is_town_exists >= 0:
            selected_district_info = district_info
            break
    return selected_district_info['name']


def find_member_with_district(city_name, district_name):
    gen_district = city_name[0:2] + ' ' + district_name
    selected_member = list(
        filter(lambda x: x['district'] == gen_district, assembly_data))[0]
    return selected_member['name_kr']


def find_member(city_name, local_name, town_name):
    return find_member_with_district(city_name, find_district_name(city_name, local_name, town_name))

member_name = find_member('서울특별시', '강동구', '강일동')
print(member_name)
