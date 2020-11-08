# -*- coding: utf-8 -*-
import scrapy, copy, re
from enum import Enum, unique
from wxit_car.items import WxitCarItem


class CiasiSpider(scrapy.Spider):
    name = 'ciasi'
    allowed_domains = ['ciasi.org.cn']
    start_urls = ['http://www.ciasi.org.cn/Home/safety/index?sid=15&bid=&cid=&sss=1&year=52,51,50,49']

    def parse(self, response):
        eval_by_item = response.xpath('//div[@class="eval_by_item"]')
        for eval_ in eval_by_item:
            e_url = eval_.xpath('./a/@href').extract_first()
            e_name = eval_.xpath('./a/div/p[@class="ev_br_t"]/text()').extract_first()
            e_factory = eval_.xpath('./a/div[@class="ev_i_manu"]/div/p/text()').extract_first()
            e_type = eval_.xpath('./a/div[@class="ev_i_models"]/div/p/text()').extract_first()
            e_level = eval_.xpath('./a/div[@class="ev_i_level"]/div/p/text()').extract_first()
            e_model = eval_.xpath('./a/div[@class="ev_i_model"]/div/p/text()').extract_first()
            if e_url:
                item = {"name": e_name, "factory": e_factory, "type": e_type, "level": e_level, "model": e_model}
                yield scrapy.Request(url=response.urljoin(e_url), callback=self.sub_parse, meta=copy.deepcopy(item))
            else:
                print("url is null %s" % e_url)
            # break

    @staticmethod
    def color_to_color(str_color):
        # 列表 字符串
        if isinstance(str_color, list):
            return list(
                map(lambda s_c: ''.join(
                    [color[color_key].value for color_key in color.__members__ if color_key in s_c]), str_color))
        else:
            raise Exception(print('str_color is not list %s' % str_color))

    def sub_parse(self, response):
        item = WxitCarItem()
        # Todo 左侧数据
        safe_title = response.xpath('//div[@class="pur_le_item"]/div[@class="pur_l_txt"]/p/text()').extract()
        safe_info = response.xpath('//div[@class="pur_le_item"]/div[@class="pur_l_rig"]/div/img/@src').extract()
        if len(safe_title) == len(safe_info) == 9:
            safe_info_color = self.color_to_color(safe_info)
            safe_info_all = list(map(lambda x, w: "{}|{}".format(x, w), safe_title, safe_info_color))
            # driver_face_airbag, front_crew_airbag, front_side_airbag, later_side_airbag, f_l_side_airbag, driver_lap_airbag, sub_driver_lap_airbag, FCW, AEB = safe_info_all
            item['sale_equip_config'] = safe_info_all
        else:
            raise Exception(print("safe_title and title_info Not equal %s" % len(safe_info)))

        # Todo 右侧数据  {"":[{车内乘员安全指数:G,details:{车内乘员安全指数:G,侧面碰撞:A}},]}
        dict_index_project, sub_all, index_flag = dict(), list(), [0, 1, 5, 6, 7]
        key = response.xpath('//div[@class="pur_item"]/p/text()').extract_first()
        sub_index_project = response.xpath('//div[@class="pr_e_lt"]/p/text()').extract()
        sub_mark_index_project = response.xpath('//div[@class="ev_i_bs"]/span/text()').extract()

        sub_detail_project = response.xpath('//div[@class="pr_t_xt"]/p/text()').extract()
        sub_mark_detail_project = response.xpath('//div[@class="pur_resu"]/div[@class="co_pu_s"]/span/text()').extract()

        for index, k_v in enumerate(zip(sub_index_project, sub_mark_index_project)):
            sub_ = self.format_data(*k_v, sub_detail_project[index_flag[index]:index_flag[index + 1]:],
                                    sub_mark_detail_project[index_flag[index]:index_flag[index + 1]:])
            sub_all.append(sub_)
        dict_index_project[key] = sub_all
        item['score_project'] = dict_index_project

        # Todo 下方数据
        item_projects = response.xpath('//div[@class="par_p_block"]//table')
        projects_list = list()
        for item_detail in item_projects:
            projects_dict = dict()
            pro_title = item_detail.xpath(
                './tr//div[@class="pa_t_ds"or @class="p_h_tx"]//p[text()!="总体评价等级"]/text()').extract_first()
            pro_level = item_detail.xpath('./tr//div[@class="pa_t_bz"]/span/text()').extract_first()
            sub_pro_title = item_detail.xpath('./tr//div[@class="pa_i_le" or @class="pa_i_xl"]/p/text()').extract()
            sub_pro_level = item_detail.xpath('./tr//div[@class="pa_i_rg" or @class="co_pu_s"]/span/text()').extract()

            extend_title = item_detail.xpath('./tr//div[@class="pa_t_it"]/p/text()').extract()
            extend_level = item_detail.xpath('./tr//div[@class="pa_i_rg"]/i/img/@src').extract()

            sub_pro_title.extend(extend_title)
            sub_pro_level.extend(extend_level)
            if len(sub_pro_title) > len(sub_pro_level):
                try:
                    sub_pro_title.remove('假人伤害')
                except ValueError as e:
                    print("list remove data null %s" % e)
                try:
                    sub_pro_title.remove('驾驶员防护')
                    sub_pro_title.remove('乘员防护')
                except ValueError as e:
                    print("list remove data null %s" % e)
            sub_list = []
            if len(sub_pro_title) == len(sub_pro_level):
                for d1, d2 in zip(sub_pro_title, sub_pro_level):
                    sub_dict = dict()
                    sub_dict[d1] = d2
                    if '气囊起爆情况' in sub_dict.keys():
                        if 'rad' in sub_dict['气囊起爆情况']:
                            sub_dict['气囊起爆情况'] = 'NO'
                        else:
                            sub_dict['气囊起爆情况'] = 'YES'
                    else:
                        pass
                    sub_list.append(sub_dict)
            else:
                for d1, d2 in zip(sub_pro_title, sub_pro_level):
                    sub_dict = dict()
                    sub_dict[d1] = d2
                    sub_list.append(sub_dict)
                print("len(sub_pro_title) != len(sub_pro_level)%s!=%s" % (len(sub_pro_title), len(sub_pro_level)))

            projects_dict[pro_title] = pro_level
            projects_dict["details"] = sub_list
            projects_list.append(projects_dict)

        item['projects_detail'] = projects_list
        sub_pro_price = response.xpath(
            '//div[@class="par_p_block"]//table//tr//div[@class="pa_bt_le"]/span/text()').extract_first()
        item['price'] = ''.join(re.findall(pattern=r'\d+.\d+', string=sub_pro_price))
        item = dict(response.meta, **item)
        yield item

    @staticmethod
    def format_data(sub_index_project, sub_mark_index_project, sub_detail_project, sub_mark_detail_project):
        sub_temp, sub_dict_temp = dict(), dict()
        sub_temp[sub_index_project] = sub_mark_index_project
        for l1, l2 in zip(sub_detail_project, sub_mark_detail_project):
            sub_dict_temp[l1] = l2
        sub_temp['details'] = sub_dict_temp
        return sub_temp


@unique
class color(Enum):
    green = "车辆标配"
    rad = "车辆选配"
    yellow = "车辆未配备"
