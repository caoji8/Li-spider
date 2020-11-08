import requests
import os
from lxml import etree
import re
import time
import json
import linecache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class lagouhtml():
    def __init__(self):
        self.chromeOptions = Options()
        self.chromeOptions._arguments = ['disable-infobars', '--headless']
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chromeOptions.add_experimental_option("prefs", prefs)
        self.filepath = r'D:\ProgramWorkSpace\PycharmProfessional\DemoData\练习二\test\url.json'
        self.getpath = os.getcwd()
        print(self.getpath)

    def parse_1(self):
        if not os.path.exists(self.getpath + '\parse_1.html'):
            starturl = 'https://www.lagou.com/'
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "user_trace_token=20190509130830-bfbbda9c-4fec-45be-b8cc-1702ffa6e7ba; _ga=GA1.2.826744677.1557378509; LGUID=20190509130830-7c8f3671-7218-11e9-9ede-5254005c3644; JSESSIONID=ABAAABAAAGGABCB152CA215841947D1D1923D278F01429E; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557378509,1557378514,1557378532; _gid=GA1.2.1546619450.1557378532; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_navigation; SEARCH_ID=ec74e919f314413fb3cfc92684396f6f; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a9b6c6502502-0c372f66ba438d-6353160-1327104-16a9b6c6503434%22%2C%22%24device_id%22%3A%2216a9b6c6502502-0c372f66ba438d-6353160-1327104-16a9b6c6503434%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; X_HTTP_TOKEN=3c2b7306a54f298a96568375512ade489dd440df31; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557386568; LGRID=20190509152250-405c0e7f-722b-11e9-9ee1-5254005c3644",
                "Host": "www.lagou.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
            }
            response = requests.get(url=starturl, headers=headers)

            print(response.apparent_encoding)
            with open(self.getpath + '\parse_1.html', 'w', encoding='utf-8')as f:
                f.write(response.text)
        else:
            print('文件已经获取！')
            with open(self.getpath + '\parse_1.html', 'r', encoding='utf-8')as f:
                parse_1 = f.read()
            return parse_1

    def info_1(self, html_1):
        selecter = etree.HTML(text=html_1)
        chlid = selecter.xpath('//div[@class="menu_box"]/div[@class="menu_sub dn"]')
        dictmenu = {}
        for menu_sub in chlid:

            menu = menu_sub.xpath('./dl/dt/span/text()')
            menuforinfo = menu_sub.xpath('./dl/dd')

            for number, url_content in enumerate(menuforinfo):
                listmenu = []
                content = url_content.xpath('./a/text()')
                url = url_content.xpath('./a/@href')
                for c_u in zip(content, url):
                    listmenu.append(list(c_u))
                dictmenu[menu[number]] = listmenu
        return dictmenu

    def parse_2(self, url, name):
        if not os.path.exists(self.getpath + '\menu_sub'):
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "user_trace_token=20190509130830-bfbbda9c-4fec-45be-b8cc-1702ffa6e7ba; _ga=GA1.2.826744677.1557378509; LGUID=20190509130830-7c8f3671-7218-11e9-9ede-5254005c3644; _gid=GA1.2.1546619450.1557378532; index_location_city=%E5%85%A8%E5%9B%BD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a9b6c6502502-0c372f66ba438d-6353160-1327104-16a9b6c6503434%22%2C%22%24device_id%22%3A%2216a9b6c6502502-0c372f66ba438d-6353160-1327104-16a9b6c6503434%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAABAABEEAAJA417439B961322EF844BD09B24680D746; SEARCH_ID=2901faa3e44f4f90a126942c428473ec; X_HTTP_TOKEN=3c2b7306a54f298a71925475512ade489dd440df31; _gat=1; LGSID=20190510094838-bae201c1-72c5-11e9-9eec-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F; LGRID=20190510094838-bae20410-72c5-11e9-9eec-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557378509,1557378514,1557378532,1557452916; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557452916",
                "Host": "www.lagou.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
            }
            response = requests.get(url=url, headers=headers)
            print(response.status_code, response.apparent_encoding)
            with open(self.getpath + '\menu_sub\{}.html'.format(name.replace('/', '')), 'w', encoding='utf-8') as f:
                f.write(response.text)
            time.sleep(10)
        else:
            # print('已经获取到menu_sub')

            with open(self.getpath + '\menu_sub\{}.html'.format(name.replace('/', '')), 'r', encoding='utf-8')as f:
                html = f.read()
            return html

    def info_2(self, url, html):
        selecter = etree.HTML(text=html)
        lista = selecter.xpath('//*[@id="s_position_list"]//div[@class="pager_container"]/a')
        # 生成可访问连接
        url_all = []
        if len(lista) == 6 and len(lista) != 0:
            url_all.append(url)  # 第一页
            for number in range(2, int(lista[-2].xpath('./text()')[0]) + 1):
                url_all.append(url + str(number) + '/')  # 后面几页
        else:
            # print(url,'丢失 ')
            pass
        return url_all

    def url_sub(self, url, keys, secondget):
        if not os.path.exists(self.getpath + '\sub_url'):
            rec = re.compile('/(\d+)/')
            if secondget >= 2:
                filename = str(int(rec.findall(url)[0]) - 1)
            else:
                filename = rec.findall(url)[0]
            filepath = self.getpath + '\sub_url\{}{}.html'.format(keys, filename)

            if not os.path.exists(filepath):
                driver = webdriver.Chrome(chrome_options=self.chromeOptions
                                          ,
                                          executable_path='D:\Program Files\Anaconda3\chromedriver_win32\chromedriver.exe')
                print('正在获取 {}'.format(url))
                try:
                    driver.get(url)
                    time.sleep(2)

                    with open(filepath, 'w', encoding='utf-8')as f:
                        f.write(driver.page_source)
                    driver.close()
                    driver.quit()
                    self.url_sub(url, keys, secondget)
                except TimeoutException:
                    print('超时 重新获取{}'.format(url))
                    self.url_sub(url, keys, secondget)
            elif os.path.getsize(filepath) / 1024 < 100:
                secondget += 1
                print('网络出错...', url)
                print('错误次数', secondget)
                os.remove(filepath)
                if secondget < 2:
                    self.url_sub(url, keys, secondget)
                else:
                    print('网页源代码不规范')
                    self.url_sub(url, keys, secondget)
        else:
            pass

    def parse_3(self, path_html):  # 返回一个页面的所有url 15个
        with open(path_html, 'r', encoding='utf-8')as f:
            html = f.read()
        selecter = etree.HTML(text=html)
        href_url = selecter.xpath(
            '//ul[@class="item_con_list"]/li[@class="con_list_item default_list"]/div[@class="list_item_top"]/div[@class="position"]/div[@class="p_top"]/a/@href')
        return href_url

    def info_3(self, url, folder,secondget):

        if secondget >= 2:
            return
        else:
            filepath = os.path.join(self.getpath + '\\info_url\\', folder + ".html")
        if not os.path.exists(filepath):
            driver = webdriver.Chrome(chrome_options=self.chromeOptions
                                      ,
                                      executable_path='D:\Program Files\Anaconda3\chromedriver_win32\chromedriver.exe')
            try:
                driver.get(url=url)

                time.sleep(6)
                with open(filepath, 'w', encoding='utf-8')as f:
                    f.write(driver.page_source)
                driver.close()
                driver.quit()
                self.info_3(url, folder,secondget)
            except TimeoutException:
                print('网络出错...')
                self.info_3(url, folder,secondget)
        elif os.path.getsize(filepath) / 1024 < 80:
            secondget += 1
            os.remove(filepath)
            if secondget < 2:
                self.url_sub(url, folder, secondget)
            else:
                print('网页源代码不规范')
                self.url_sub(url, folder, secondget)

    def main1(self):
        if not os.path.exists(self.getpath + r'\test\url.json'):
            parse_1 = self.parse_1()
            dictmenu = self.info_1(parse_1)
            list_all_end = []

            for keys, values in dictmenu.items():

                for start_url in values:
                    dict_all_end = {}
                    # print('正在获取:{}'.format(start_url[0]))
                    html = self.parse_2(start_url[1], start_url[0])
                    url_all = self.info_2(start_url[1], html)  # 可能为空
                    dict_all_end[start_url[0]] = url_all
                    if not url_all == []:
                        list_all_end.append(dict_all_end)

            for sub in list_all_end:
                for keys, values in sub.items():
                    print('正在获取 {} 所有页面内容'.format(keys))
                    main_key = str(keys).replace('/', '')

                    for sub_url in values[1:]:
                        secondget = 0
                        self.url_sub(sub_url, main_key, secondget)
        else:
            print('json文件已经存在不需要操作！')

        if not os.path.exists(self.getpath + r'\test'):
            for menu_root, menu_dirs, menu_files in os.walk(
                    r'D:\ProgramWorkSpace\PycharmProfessional\DemoData\练习二\menu_sub'):

                for q, menu_file in enumerate(menu_files):
                    dict_all_url = {}
                    list_all_url = []
                    menu_url = self.parse_3(os.path.join(menu_root, menu_file))
                    list_all_url.append(menu_url)
                    menu_key = menu_file.replace('.html', '')

                    for sub_root, sub_dirs, sub_files in os.walk(
                            r'D:\ProgramWorkSpace\PycharmProfessional\DemoData\练习二\sub_url'):
                        for sub_file in sub_files:
                            if sub_file.endswith('.html') and menu_key in sub_file:
                                htmlpath = os.path.join(r'D:\ProgramWorkSpace\PycharmProfessional\DemoData\练习二\sub_url',
                                                        sub_file)
                                sub_url = self.parse_3(os.path.join(sub_root, htmlpath))
                                list_all_url.append(sub_url)
                    dict_all_url[menu_key] = list_all_url
                    print(dict_all_url)
                    with open(self.getpath + r'\test\url.json', 'a+', encoding="utf-8")as f:

                        f.write(json.dumps(obj=dict_all_url, ensure_ascii=False) + '\n')
        else:
            print('json文件已经写入！')

        # for sequence,work in enumerate():
        #
        #     json.loads(self.f.readline())
        #     print('正在处理第%d行数据 %s'%(sequence+1,work))
        count = 1
        pathfile = self.getpath + '\info_url'
        while True:
            url_dict_json = linecache.getline(self.filepath, count)
            if url_dict_json == '':
                break
            count += 1
            url_dict = json.loads(url_dict_json)
            # 创建文件夹/遍历列表
            for url_key, url_list in url_dict.items():

                if os.path.exists((os.path.join(pathfile, url_key))):
                    for urls in url_list:
                        for url in urls:
                            print('正在获取 %s 相关信息 %s' % (url_key, url))
                            reg = re.compile('/(\d+)\.html')
                            filename = url_key + '\\' + reg.findall(url)[0]
                            secondget=0
                            self.info_3(url=url, folder=filename,secondget=secondget)
                else:
                    os.mkdir(os.path.join(pathfile, url_key))

if __name__ == '__main__':
    lagouhtml = lagouhtml()
    lagouhtml.main1()
