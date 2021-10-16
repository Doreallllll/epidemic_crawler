"""数据采集"""

import json
import re
import requests
from bs4 import BeautifulSoup


class BaseCrawler():
    """基础类"""
    def __init__(self, target_url):
        """初始化 变量赋值
        
        Args:
            target_url (str): 目标爬取网站
        """
        self.target_url = target_url
        return
    
    def get_content_from_url(self, url):
        """请求url 获取响应内容的字符串数据

        Args:
            url (string): 目标url

        Returns:
            请求响应内容字符串
        """
        # http请求
        resp = requests.get(url)
        # 返回网页响应内容
        return resp.content.decode()
    
    def parse_homepage_content(self, homepage_content, find_id):
        """解析目标网站主页数据

        Args:
            homepage_content (string): 主页内容
            find_id (string): bs4匹配id

        Returns:
            结构化数据
        """
        # 使用lxml进行解析
        soup = BeautifulSoup(homepage_content, 'lxml')
        # 根据id提取指定内容
        script = soup.find(id=find_id)
        # 正则 去除多余的字符 提取json字符串
        json_str = re.findall(r'\[.+\]', script.text)[0]
        # json反序列化
        return json.loads(json_str)


class Crawler(BaseCrawler):
    
    def _get_last_day_data_of_world(self, homepage_content):
        """获取世界各国最近一日疫情数据

        Args:
            home_page_content (string): 主页内容

        Returns:
            结构化数据
        """
        return self.parse_homepage_content(homepage_content, 'getListByCountryTypeService2true')
    
    def _get_last_day_data_of_china(self, homepage_content):
        """获取中国各省最近一日疫情数据

        Args:
            home_page_content (string): 主页内容

        Returns:
            结构化数据
        """
        return self.parse_homepage_content(homepage_content, 'getAreaStat')
    
    def crawl_last_day_data_of_world(self):
        """采集最近一日世界各国疫情数据
                
        Returns:
            结构化数据
        """
        # 请求首页数据
        homepage_content = self.get_content_from_url(self.target_url)
        # 解析首页数据，获取最近一日疫情数据
        data = self._get_last_day_data_of_world(homepage_content)
        return data
    
    def crawl_last_day_data_of_china(self):
        """采集最近一日全国各省疫情数据
        
        Returns:
            结构化数据
        """
        # 请求首页数据
        homepage_content = self.get_content_from_url(self.target_url)
        # 解析首页数据，获取最近一日疫情数据
        data = self._get_last_day_data_of_china(homepage_content)
        return data
    
    def _get_all_data(self, data):
        """数据处理

        Args:
            data (dict): 近一日数据

        Returns:
            ret: k-国家名 v-国家历史疫情数据
        """
        ret = []
        # 遍历疫情数据，获取统计的url
        for item in data:
            # 获取目标数据的url
            statistics_data_url = item['statisticsData']
            # 请求获取各国、省份历史数据
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            # 数据结构化
            statistics_data = json.loads(statistics_data_json_str)
            # 获取国家/省份名称
            statistics_data['provinceName'] = item['provinceName']
            # 将数据存入ret中
            ret.append(statistics_data)
        return ret
    
    
    def crawl_all_data_of_world(self, last_day_data_of_world):
        """采集历史以来世界各国疫情数据
        
        Args:
            last_day_data_of_world (dict): 世界各国近一日数据
        """
        return self._get_all_data(last_day_data_of_world)
    
    def crawl_all_data_of_china(self, last_day_data_of_china):
        """采集历史以来全国各省疫情数据
        
        Args:
            last_day_data_of_china (dict): 国内各省近一日数据
        """ 
        return self._get_all_data(last_day_data_of_china)