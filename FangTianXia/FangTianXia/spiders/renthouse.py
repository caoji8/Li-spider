# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import json
from copy import deepcopy
from FangTianXia.items import FangtianxiaItem


class RenthouseSpider(scrapy.Spider):
    name = 'renthouse'
    allowed_domains = ['fang.com']
    start_urls = ['https://hf.esf.fang.com/school/']

    def judge_city(self, key, url):
        return {
            key: lambda key: key in url,
        }[key](url)

    def parse(self, response):
        school_list = response.xpath(
            '//div[@class="schoollist"]//p[@class="title"]/a')
        if self.judge_city("hf", response.url):
            response.meta["city"] = "合肥"

        for school in school_list:
            school_name = school.xpath('./text()').extract_first()
            school_url = response.urljoin(
                school.xpath('./@href').extract_first())
            print("正在获取...{}".format(school_name))
            if school_url:
                yield scrapy.Request(url=school_url, callback=self.school_parse, meta=deepcopy({"入口学校": school_name}))
        # Todo 翻页
        next_page = response.xpath(
            '//*[@id="PageControl1_hlk_next"]/@href').extract_first()
        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def school_parse(self, response):
        school_name = response.meta["入口学校"]
        print("入口学校", school_name)

        school_type = response.xpath(
            '//p[@class="schoolname"]/span[@class="info gray9 ml10"]/text()').extract_first()
        school_type = "".join(
            list(map(lambda x: re.sub(r"\s|]|\[", "", x), school_type)))
        print("学校类别", school_type)

        sale_house = response.xpath(
            '//div[@class="info floatr"]/ul/li[@class="buttonLi"]//strong/text()').extract_first()
        print("在售房源", sale_house)

        school_address = response.xpath(
            '//div[@class="info floatr"]/ul/li[@style][3]/text()').extract_first()
        print("学校地址", school_address)

        around_house = response.xpath(
            '//div[@class="info floatr"]/ul/li[@style][4]/span[@class="pr5"]/text()').extract()
        around_house = "|".join(around_house)
        print("周边小区", around_house)

        school_feature = response.xpath(
            '//div[@class="info floatr"]/ul/li[@style][5]/span[@class="pr5"]/text()').extract()
        school_feature = '|'.join(school_feature)
        print("学校特色", school_feature)

        # Todo None
        rise_study = response.xpath(
            '//div[@class="info floatr"]/ul/li[@class="school"]/p/a/text()').extract()
        rise_study = '|'.join(rise_study)
        print("升学情况", rise_study)

        brief_url = response.urljoin(response.xpath(
            '//a[@id="profile"]/@href').extract_first())
        print("招生范围链接", brief_url)

        s_range = None
        if brief_url:
            s_range = self.school_range_parse(url=brief_url)

        house_list = response.xpath('//ul[@class="houselist"]/li')
        for house in house_list:
            house_name = house.xpath(
                './div[@class="houseInfo"]/h3/a[@class="title"]/text()').extract_first()
            house_url = response.urljoin(
                house.xpath('./div[@class="houseInfo"]/h3/a[@class="title"]/@href').extract_first())
            distance_temp = house.xpath(
                './div[@class="houseInfo"]/p/text()').re(r"\d.\d+km")
            distance = None
            if distance_temp:
                distance = distance_temp[0]
            print("小区名称", house_name)
            print("待爬地址", house_url)
            print("距离学校", distance)
            meta = {"入口学校": school_name, "学校类别": school_type, "在售房源": sale_house, "学校地址": school_address,
                    "周边小区": around_house, "学校特色": school_feature, "升学情况": rise_study, "小区名称": house_name,
                    "距离学校": distance, "招生范围": s_range, "招生范围链接": brief_url, "房源详情链接": house_url}
            if house_url:
                yield scrapy.Request(url=house_url, callback=self.house_detail_parse, meta=deepcopy(meta))

        # Todo 可能要翻页
        # all_page_temp = response.xpath('//*[@id="pageCount"]/text()').re(r'\d+')
        # all_page = all_page_temp[0] if all_page_temp else None
        #
        # present_page = response.xpath('//*[@id="page"]/a[@class="pageNow"]/text()').extract_first()
        # print( all_page, present_page, len(house_list))
        if len(house_list) == 20:
            # 从连接中提取数字
            reg_url = re.compile(r'(\d+).htm')
            url_extract_number = reg_url.search(response.url)
            # 判断要翻多少页
            if url_extract_number:
                url_next_temp = "{}{}/xiaoqu/{}".format(
                    self.start_urls[0], url_extract_number.group(1), 1)
                headers = {
                    "accept-encoding": "gzip, deflate",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                result = requests.get(
                    url=url_next_temp, headers=headers).json()
                all_page_number = int(result["ProjCount"])
                present_page = int(all_page_number / 20)
                for page_number in range(2, present_page + 2):
                    page_url = "{}{}/xiaoqu/{}".format(
                        self.start_urls[0], url_extract_number.group(1), page_number)
                    print("page_url", page_url)
                    meta = {"入口学校": school_name, "学校类别": school_type, "在售房源": sale_house, "学校地址": school_address,
                            "周边小区": around_house, "学校特色": school_feature, "升学情况": rise_study, "招生范围": s_range,
                            "招生范围链接": brief_url}
                    yield scrapy.Request(url=page_url, callback=self.house_next_parse, meta=deepcopy(meta))

    def house_next_parse(self, response):
        house_list_json = json.loads(response.text)
        # "小区名称": house_name,
        # "距离学校": distance,
        # "房源详情链接": house_url
        for house_dict in house_list_json["ProjInfo"]:
            house_name = house_dict["projName"]
            distance = house_dict["projDistance"]
            house_url = house_dict["projUrl"]
            response.meta["小区名称"] = house_name
            response.meta["距离学校"] = distance
            response.meta["房源详情链接"] = response.urljoin(house_url)
            if house_url and house_url != "//":
                yield scrapy.Request(url=response.meta["房源详情链接"], callback=self.house_detail_parse, meta=deepcopy(response.meta))

    def school_range_parse(self, url):
        headers = {
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        result = requests.get(url=url, headers=headers)
        regx = re.compile(r'<dt>招生范围.*?<p style=".*?">(.*?)</p>', re.S)
        result = regx.search(result.text)
        s_range = None
        if result:
            s_range = result.group(1).replace(
                "\n", '').replace(' ', '').replace("\r", '')
        print("招生范围", s_range)
        return s_range

    def data_map_filter(self, list_map_filter, replace_str):
        map_end = list(map(lambda x: re.sub(
            r"\s{}".format(replace_str), "", x), list_map_filter))
        filter_end = list(filter(lambda x: x != '', map_end))
        return filter_end

    def house_detail_parse(self, response):
        house_price_temp = response.xpath(
            '//div[@class="Rbiginfo"]//text()').extract()
        house_price_filter = self.data_map_filter(house_price_temp, "|贷款计算器")
        house_price = None
        increase_price = None
        if len(house_price_filter) == 5:
            house_price = ''.join(house_price_filter[:3])
            increase_price = ''.join(house_price_filter[3:])
        elif len(house_price_filter) == 3:
            house_price = ''.join(house_price_filter)
        print("售价", house_price)
        print("环比涨幅", increase_price)

        house_detail_temp = response.xpath(
            '//div[@class="Rinfolist"]//text()').extract()
        house_detail_filter = self.data_map_filter(house_detail_temp, '')
        print("house_detail_filter", house_detail_filter)
        build_year, build_type, house_address, developer, wy_company, user_num, ok_school = None, None, None, None, None, None, None
        number1 = [i for i, x in enumerate(house_detail_filter) if x == '建筑年代']
        if number1:
            build_year = house_detail_filter[number1[0] + 1]
        number2 = [i for i, x in enumerate(house_detail_filter) if x == '建筑类型']
        if number2:
            build_type = house_detail_filter[number2[0] + 1]
        number3 = [i for i, x in enumerate(house_detail_filter) if x == '小区位置']
        if number3:
            house_address = house_detail_filter[number3[0] + 1]
        number4 = [i for i, x in enumerate(house_detail_filter) if x == '开发商']
        if number4:
            developer = house_detail_filter[number4[0] + 1]
        number5 = [i for i, x in enumerate(house_detail_filter) if x == '物业公司']
        if number5:
            wy_company = house_detail_filter[number5[0] + 1]
        number6 = [i for i, x in enumerate(house_detail_filter) if x == '房屋总数']
        if number6:
            user_num = house_detail_filter[number6[0] + 1]
        number7 = [i for i, x in enumerate(house_detail_filter) if x == '对口学校']
        if number7:
            ok_school = "|".join(house_detail_filter[number7[0] + 1:])

        old_house = response.xpath(
            '//div[@id="xqwxqy_C01_16"]/a[1]/div[contains(@class,"std")]/p[@class]/text()').extract_first()
        ok_house = response.xpath(
            '//div[@id="xqwxqy_C01_16"]/a[2]/div[contains(@class,"std")]/p[@class]/text()').extract_first()
        rent_house = response.xpath(
            '//div[@id="xqwxqy_C01_16"]/a[3]/div[contains(@class,"std")]/p[@class]/text()').extract_first()

        active_level = response.xpath(
            '//div[@class="s3"]/p[1]/text()').extract_first()
        plate_level = response.xpath(
            '//div[@class="s3"]/p[2]/text()').extract_first()
        wy_level = response.xpath(
            '//div[@class="s3"]/p[3]/text()').extract_first()
        education_level = response.xpath(
            '//div[@class="s3"]/p[4]/text()').extract_first()

        # url new_code
        url_new_code = response.xpath(
            '//*[@id="iframe_map"]/@src').extract_first()
        response.meta["url_new_code"] = url_new_code

        response.meta["售价"] = house_price
        response.meta["环比涨幅"] = increase_price
        response.meta["建筑年代"] = build_year
        response.meta["建筑类型"] = build_type
        response.meta["小区位置"] = house_address
        response.meta["开发商"] = developer
        response.meta["物业公司"] = wy_company
        response.meta["房屋总数"] = user_num
        response.meta["对口学校"] = ok_school
        response.meta["二手房源"] = old_house
        response.meta["最近成交"] = ok_house
        response.meta["租房房源"] = rent_house
        response.meta["活跃度评级"] = active_level
        response.meta["板块评级"] = plate_level
        response.meta["物业评级"] = wy_level
        response.meta["教育评级"] = education_level
        # Todo 物业费
        level_url = response.urljoin(response.xpath(
            '//span[@class="rother"]/a/@href').extract_first())
        print("物业费...", level_url)
        if level_url:
            yield scrapy.Request(url=level_url, callback=self.house_wy_parse, meta=deepcopy(response.meta))

    def house_wy_parse(self, response):
        wy_price = response.xpath(
            '/html/body/div[2]/div[4]/div[2]/div[2]/ol/li[1]/div/span[1]/span[2]/text()').extract_first()

        response.meta["物业服务费"] = wy_price
        coord_url = response.urljoin(response.meta["url_new_code"])
        #  todo 经纬度
        yield scrapy.Request(url=coord_url, callback=self.house_coord_parse, meta=deepcopy(response.meta))

    def house_coord_parse(self, response):
        item = FangtianxiaItem()
        regx = re.compile(r'"baidu_coord_x":"(\d+.\d+)"')
        regy = re.compile(r'"baidu_coord_y":"(\d+.\d+)"')

        coord_x = regx.search(response.text)
        coord_y = regy.search(response.text)
        x_ = None
        y_ = None
        if coord_x and coord_y:
            x_ = coord_x.group(1)
            y_ = coord_y.group(1)
        response.meta["纬度"] = x_
        response.meta["经度"] = y_

        item["school_name"] = response.meta["入口学校"]
        item["ok_school"] = response.meta["对口学校"]
        item["school_type"] = response.meta["学校类别"]
        item["sale_house"] = response.meta["在售房源"]
        item["school_address"] = response.meta["学校地址"]
        item["around_house"] = response.meta["周边小区"]
        item["school_feature"] = response.meta["学校特色"]
        item["rise_study"] = response.meta["升学情况"]
        item["house_name"] = response.meta["小区名称"]
        item["distance"] = response.meta["距离学校"]
        item["s_range"] = response.meta["招生范围"]
        item["house_price"] = response.meta["售价"]
        item["increase_price"] = response.meta["环比涨幅"]
        item["increase_some"] = None
        item["build_year"] = response.meta["建筑年代"]
        item["build_type"] = response.meta["建筑类型"]
        item["house_address"] = response.meta["小区位置"]
        item["x_"] = response.meta["纬度"]
        item["y_"] = response.meta["经度"]
        item["developer"] = response.meta["开发商"]
        item["wy_company"] = response.meta["物业公司"]
        item["user_num"] = response.meta["房屋总数"]
        item["old_house"] = response.meta["二手房源"]
        item["ok_house"] = response.meta["最近成交"]
        item["rent_house"] = response.meta["租房房源"]
        item["active_level"] = response.meta["活跃度评级"]
        item["plate_level"] = response.meta["板块评级"]
        item["wy_level"] = response.meta["物业评级"]
        item["education_level"] = response.meta["教育评级"]
        item["wy_price"] = response.meta["物业服务费"]
        item["city"] = response.meta["物业服务费"]

        yield item
