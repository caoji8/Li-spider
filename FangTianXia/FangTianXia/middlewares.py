# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
from fake_useragent import UserAgent


class UserAgentDownloadMiddleware(object):
    def process_request(self, request, spider):
        # time.sleep(0.5)
        user_agent = UserAgent().random
        request.headers['Cookie']='global_cookie=5aod3o6e8b16dt5eupif97mxq10k53kb9fl; searchConN=1_1582943726_632%5B%3A%7C%40%7C%3A%5De35bfe75acd487e8139af416fd8d2588; new_search_uid=03d475944d9fa888c69c34d9fad8633c; newhouse_user_guid=B5126C8D-39DC-5DEC-CB3B-3C016839727B; Integrateactivity=notincludemc; integratecover=1; lastscanpage=0; global_wapandm_cookie=2owz4l87z3g1j694958h4xxd710k7cuye0w; UM_distinctid=170a4eb725a59f-03effd57fd722c-4313f6b-144000-170a4eb725b5bf; __utma=147393320.1968134039.1579051757.1583414377.1583478983.22; __utmz=147393320.1583478983.22.14.utmcsr=fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/default.htm; city=xm; ASP.NET_SessionId=eqdw01byskznlgg00qrh3fxr; g_sourcepage=zf_fy%5Exq_pc; __utmc=147393320; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.18.10.1583478983; unique_cookie=U_1qtezgr9fr8jyq4b875xsxyjz10k7fvo8n7*2'
        request.headers["User-Agent"] = user_agent
