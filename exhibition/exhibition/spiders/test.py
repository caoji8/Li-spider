# -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
# import requests
#
# url = 'http://ip.chinaz.com/'
# proxies = {
#     'http': 'http://110.243.3.20:9999',
#     }
# r = requests.get(url, proxies=proxies)
# soup = BeautifulSoup(r.text, 'lxml')
# parent_node = soup.find(class_="IpMRig-tit")
# for i in parent_node.find_all('dd'):
#     print(i.get_text())