# encoding:utf-8
# Time:2020/3/20
# File:dome01.py
from fake_useragent import UserAgent
dict_info = {'active_level': '本小区2月活跃度为7.41,较上月活跃度上升,属于不活跃小区',
             'around_house': '7个小区',
             'build_type': '塔楼',
             'build_year': '2003年建成',
             'developer': None,
             'distance': '0.42km',
             'education_level': '一类优质学区',
             'house_address': '环城南路46号',
             'house_name': '徽京剧团宿舍',
             'house_price': '03月参考价27658元/㎡',
             'increase_price': '环比上月↑2.63%',
             'increase_some': None,
             'ok_house': '0套',
             'old_house': '2套',
             'plate_level': '成熟板块',
             'rent_house': '0套',
             'rise_study': None,
             's_range': '长江中路以南，金寨路以东，徽州大道以西，环城南路以北。',
             'sale_house': '55',
             'school_address': '徽州大道169号',
             'school_feature': '专业学科类',
             'school_name': '南门小学',
             'school_type': '小学|国家重点|公立',
             'user_num': None,
             'wy_company': None,
             'wy_level': '物业一般',
             'wy_price': '0.5元/平米·月',
             'x_': '117.33912658691406',
             'y_': '31.86761474609375'}

# import openpyxl
# writer = openpyxl.load_workbook(r"F:\PyCharmProjects\FangTianXia\test_dome\data_ 1.xlsx")
# table = writer["Sheet1"]
# table=writer.active
# nrows = table.max_row
# ncolumns = table.max_column
#
# def foo(key,value,number):
#     return {
#             key: lambda key: table.cell(row=nrows+1,column=number,value=value),
#     }[key](number)
#
# for index in range(1,ncolumns+1):
#     number=[i for i, x in enumerate(dict_info.keys()) if x == table.cell(row=2, column=index).value][0]
#     foo(key=list(dict_info.keys())[number],value=list(dict_info.values())[number],number=index)
#     writer.save(r"F:\PyCharmProjects\FangTianXia\test_dome\data_ 1.xlsx")

# print(int(30/20))
# for i in range(2,1+int(21/20)):
#     print(i)
import requests
# import
# headers = {
#     "accept-encoding": "gzip, deflate",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
# }
# result = requests.get(url="https://hf.esf.fang.com/school/5916/xiaoqu/1", headers=headers).json()
# all_page_number = result["ProjCount"]
# print(all_page_number)
# from urllib.parse import urljoin
# print(urljoin("https://hf.esf.fang.com/school/10479/xiaoqu/2","//"))
# print("hf" in "https://hf.esf.fang.com/school/")
#
#
# def foo(key, url):
#     return key in url
#
# print(foo("" , "https://hf.esf.fang.com/school/"))

print("/"in '/house/s/b914/')