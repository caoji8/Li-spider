import requests
from requests.exceptions import RequestException
import json


class liu_work():
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'acw_tc=76b20ffc15536514820815291e59814f375891fbd81a3190ea2e4bef3bb853; auth=0102DBCF84C456B2D608FEDB8FEEEE1FB3D6080016350078002D002D006100670032006F006400700074006E006D00780033006600780077007A006D006C00610000012F00FF03D4C87FE3F923F05E0CD5E44996A2A1ABCEC3D0; token=3oeiab2qo5hgurb7ucfumg',
            'Host': 'mooc.icve.com.cn',
            'Origin': 'https://mooc.icve.com.cn',
            'Referer': 'https://mooc.icve.com.cn/design/workExam/test/test.html?courseOpenId=zhiavypu41hjrdet9yxeq',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.headers_detail = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'acw_tc=76b20ffc15536514820815291e59814f375891fbd81a3190ea2e4bef3bb853; auth=0102DBCF84C456B2D608FEDB8FEEEE1FB3D6080016350078002D002D006100670032006F006400700074006E006D00780033006600780077007A006D006C00610000012F00FF03D4C87FE3F923F05E0CD5E44996A2A1ABCEC3D0; token=3oeiab2qo5hgurb7ucfumg',
            'Host': 'mooc.icve.com.cn',
            'Origin': 'https://mooc.icve.com.cn',
            'Referer': 'https://mooc.icve.com.cn/design/workExam/test/testPreview.html?courseOpenId=zhiavypu41hjrdet9yxeq&homeworkId=2996avypurvaiqo1pluqg&test=1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        file_DanXT = '/home/hadoop/桌面/pycharmwork/liuwork/DanXT.txt'
        file_DuoXT = '/home/hadoop/桌面/pycharmwork/liuwork/DuoXT.txt'
        file_PanDT = '/home/hadoop/桌面/pycharmwork/liuwork/PanDT.txt'

        self.f1 = open(file_DanXT, 'w', encoding='utf-8')
        self.f2 = open(file_DuoXT, 'w', encoding='utf-8')
        self.f3 = open(file_PanDT, 'w', encoding='utf-8')

    def get_page_start(self):
        url = 'https://mooc.icve.com.cn/design/test/getTestList'
        data = {
            'courseOpenId': 'zhiavypu41hjrdet9yxeq',
            'test': 1,
            'page': 1,
            'pageSize': 500,
        }
        try:
            re = requests.post(url=url, data=data, headers=self.headers)
            if re.status_code == 200:
                return re.text
        except RequestException:
            print('首页获取失败')
            return None

    def parse_start_json(self, start_json):
        listinfo = []
        start_js = json.loads(start_json).get('list')
        for id_data in start_js:
            if 'Id' in id_data.keys():
                item = {}
                item['Title'] = id_data.get('Title')
                item['Id'] = id_data.get('Id')
                listinfo.append(item)
        return listinfo

    def get_page_detail(self, data):
        url = 'https://mooc.icve.com.cn/design/HomeworkExamTest/preview'
        try:
            re = requests.post(url=url, data=data, headers=self.headers_detail)
            if re.status_code == 200:
                return re.text
        except RequestException:
            print('题目获取失败')

    def parse_subject_info(self, subject_info):

        subject_info = json.loads(subject_info)

        if 'questions' in subject_info.get('paperData').keys():
            for subject_data in subject_info.get('paperData').get('questions'):
                if subject_data.get('questionType') == 1:  # 单选题
                    self.DanXT(subject_data)
                if subject_data.get('questionType') == 2:  # 多选题
                    self.DuoXT(subject_data)
                if subject_data.get('questionType') == 3:  # 判断题
                    self.PanDT(subject_data)

    def DanXT(self, subject_data):  # 字典
        self.f1.write('题目:' + subject_data.get('TitleText') + '\n')
        for answer in subject_data.get('answerList'):
            self.f1.write(answer['Content'].replace('<p>', '').replace('</p>', '') + '\n')
        self.f1.write(
            '答案:' + subject_data.get('Answer').replace('0', 'A').replace('1', 'B').replace('2', 'C').replace('3',
                                                                                                             'D') + '\n')
        self.f1.write('------------------------------------------------------\n')

    def DuoXT(self, subject_data):
        self.f2.write('题目：' + subject_data.get('TitleText') + '\n')
        for answer in subject_data.get('answerList'):
            self.f2.write(answer['Content'].replace('<p>', '').replace('</p>', '') + '\n')
        self.f2.write(
            '答案：' + subject_data.get('Answer').replace('0', 'A').replace('1', 'B').replace('2', 'C').replace('3',
                                                                                                             'D') + '\n')
        self.f2.write('------------------------------------------------------\n')

    def PanDT(self, subject_data):
        self.f3.write('题目：' + subject_data.get('TitleText') + '\n')
        self.f3.write('答案：' + subject_data.get('Answer').replace('0', '错误').replace('1', '正确') + '\n')
        self.f3.write('------------------------------------------------------\n')

    def main(self):
        start_json = self.get_page_start()
        listinfo = self.parse_start_json(start_json)
        for id_data in listinfo:
            id = id_data.get('Id')
            data = {
                'courseOpenId': 'zhiavypu41hjrdet9yxeq',
                'homeworkId': id,
                'test': 1
            }
            subject_info = self.get_page_detail(data)
            self.parse_subject_info(subject_info)

        self.f1.close()
        self.f2.close()
        self.f3.close()


if __name__ == '__main__':
    liu_work = liu_work()
    liu_work.main()
