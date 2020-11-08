import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class job():
    def __init__(self):
        self.chromeOptions = Options()
        self.chromeOptions._arguments = ['disable-infobars', '--headless']
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chromeOptions.add_experimental_option("prefs", prefs)
    def response(self,i):
        if not os.path.exists(r'F:\ProgramWork\PyCharmProjects\untitled\test'):
            url='https://search.51job.com/list/070200%252C00,000000,0000,00,9,99,%2B,2,{}.html'.format(i)
            driver = webdriver.Chrome(chrome_options=self.chromeOptions
                                      ,
                                      executable_path='D:\Program Files\Anaconda3\chromedriver.exe')
            driver.get(url)
            with open(r'F:\ProgramWork\PyCharmProjects\untitled\test\{}.html'.format(i),'w',encoding='utf8')as f:
                f.write(driver.page_source)
            time.sleep(1)

            print(i+'写入成功')
        else:
            print('ok')
    def info_funtype(self):
        driver = webdriver.Chrome(chrome_options=self.chromeOptions
                                  ,
                                  executable_path='D:\Program Files\Anaconda3\chromedriver.exe')
        driver.get('https://js.51jobcdn.com/in/js/2016/layer/funtype_array_c.js?20181030')

        suop=BeautifulSoup(driver.page_source)
        funtype = suop.pre.string[75:][:-2].split(":")
        str=''.isdigit()
        print(funtype)
        dict_info=[]#岗位名称
        for i  in funtype:
            if  not i.replace('\n','').isdigit():
                info=i.split('\n')[0]
                dict_info.append(info)

    def info_arr(self):


    def info_1(self,i):
        with open(r'F:\ProgramWork\PyCharmProjects\untitled\test\{}.html'.format(i),'r',encoding='utf8')as f:
            info=f.read()
        # selector=ET.fromstring(info)
        # sele=selector.findall('//div[@class="dw_table"]/div[@class="el"]')




    def main(self):
        for i in range(16):
            self.response(str(i))
            self.info_1(str(i))
        self.info_funtype()


if __name__ == '__main__':
    job=job()
    job.main()