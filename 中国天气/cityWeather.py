import requests
import os
from os.path import join
from bs4 import BeautifulSoup
import re

#http://mobile.weather.com.cn/data/sk/101010100.html
#http://wthrcdn.etouch.cn/weather_mini?citykey=101010100

class cityWeather(object):
    def __init__(self):
        self.home_path=os.getcwd()
        self.file_path='F:\ProgramWork\PyCharmProjects\中国天气\cityweather'

    def paserWeather(self,json_info):
        pass

    def reqWeather(self,idCity,url):
        print('正在获取 %s 信息'%(idCity[1]))
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        try:
            print(url)
            req=requests.get(url=url,headers=header)
            if req.status_code==200:
                with open(os.path.join(self.file_path,'%s.json'%(idCity[1])),'w',encoding='utf-8')as f:
                    f.write(req.text)
        except Exception:
            print('获取出错')

    def paserCity(self,cityHTML):
        soup=BeautifulSoup(cityHTML,'lxml')
        infoBox=soup.find_all('div',attrs={'id':'blog_content','class':'hide-main-content'})[0]
        br=infoBox.get_text()
        regCity=re.compile('(\d{9})=(.*)')
        info=regCity.findall(br,re.S)
        return info

    def reqCity(self,url):
        if not os.path.exists(join(self.home_path,'weather.html')):
            headers={
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                        "accept-encoding": "gzip, deflate, br",
                        "accept-language": "zh-CN,zh;q=0.9",
                        "cache-control": "max-age=0",
                        "cookie": "BAIDU_SSP_lcr=https://www.baidu.com/link?url=a_lyJdz7sq9Qs7QrxBS9ZZakuIhbPeTRDrcRk-EKVGaWy-ndlmCcuRMXxVbX3rFH&wd=&eqid=a32bfb290000225f000000065ce63e9f; _javaeye_cookie_id_=1558329275681673; _ga=GA1.2.890124297.1558329276; _javaeye3_session_=BAh7BjoPc2Vzc2lvbl9pZCIlOTI2ZGIxMWQyMjVlMTMxZGE5ZjE4Nzk2YTQ5YjkyODg%3D--1cb29a6a91c72453be7e3419a3f59783365520b5; Hm_lvt_e19a8b00cf63f716d774540875007664=1558329275,1558593224; Hm_lpvt_e19a8b00cf63f716d774540875007664=1558593224; _gid=GA1.2.1548553621.1558593225; _gat_gtag_UA_127895514_6=1; dc_tos=pry288; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1558593225; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1558593225",
                        "if-none-match": "7a75e88b64c6d618d6d61bd825414371",
                        "upgrade-insecure-requests":"1",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            }
            req=requests.get(url=url,headers=headers)
            with open(join(self.home_path,"weather.html"),'wb')as fb:
                fb.write(req.content)
        else:
            print('已经获取City')
            with open(join(self.home_path,"weather.html"),'r',encoding='utf-8',errors='ignore')as fb:
                html=fb.read()
            return html


    def main(self):
        urlITeye='https://vyphn.iteye.com/blog/850431'

        cityHTML=self.reqCity(url=urlITeye)
        listCity=self.paserCity(cityHTML)
        if not os.path.exists(self.file_path):
            for city in listCity:

                    urlWeather = 'http://wthrcdn.etouch.cn/weather_mini?citykey={}'.format(city[0])
                    self.reqWeather(idCity=city,url=urlWeather)
        else:
            print('数据已经获取！')

        for city in os.listdir(self.file_path):
            with open(os.path.join(self.file_path,city),'r',encoding='utf-8')as f:
                json_info=f.read()
            if not len(json_info)==32:
                with open(os.path.join(self.home_path, 'AllCity.json'), 'a', encoding='utf-8')as f:
                    f.write(json_info+'\n')
            # self.paserWeather(json_info)

if __name__ == '__main__':
    cityweather=cityWeather()
    cityweather.main()
