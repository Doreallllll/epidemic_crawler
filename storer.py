"""数据存储"""
import pymongo
import json

from consts import KIND_WORLD, KIND_CHINA


class Storer():
    # db ip
    MG_IP = "localhost" 
    # db 端口
    MG_Port = 27017  
    # db 数据库名称
    MG_DBName = "epidemic" 
    
    def __init__(self):
        """初始化 mongodb建立连接
        """
        client = pymongo.MongoClient(f'mongodb://%s:%s/' % (self.MG_IP, self.MG_Port))
        self.db = client[self.MG_DBName]
        return
    
    def _get_col(self, k):
        return self.db[k]
    
    def save_file(self, data, path):
        """数据持久化

        Args:
            data (dict): 内容
            path (str): 路径
        """
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        return
    
    def _insert_data(self, k, data):
        """插入数据到MongoDB
        
        Args: 
            k (string): DB集合名称
            data (list): 数据序列
        """
        col = self._get_col(k)
        col.insert_many(data)
        return
    
    def _find_data(self, k):
        """查询数据
        
        Args: 
            k (string): DB集合名称
            
        Returns:
            查询得到的数据
        """
        col = self._get_col(k)
        data = []
        for i in col.find():
            data.append(i)
        return data
        
    def _get_last_day_data_key(self, kind):
        """获取近一日数据DB存储的集合名

        Args:
            kind (string): 类型 world/china
        """
        return "last_day_data_%s" % kind
    
    def _get_all_data_key(self, kind):
        """获取历史数据DB存储的集合名

        Args:
            kind (string): 类型 world/china
        """
        return "all_data_%s" % kind

    def set_last_day_data(self, kind, data):
        k = self._get_last_day_data_key(kind)
        self._insert_data(k, data)
        return
    
    def get_last_day_data(self, kind):
        k = self._get_last_day_data_key(kind)
        return self._find_data(k)

    def set_all_data(self, kind, data):
        k = self._get_all_data_key(kind)
        self._insert_data(k, data)
        return
    
    def get_all_data(self, kind):
        k = self._get_all_data_key(kind)
        return self._find_data(k)
    

class DataHandler(Storer):
    
    def _sort_by_key(self, data, key):
        """对指定key的值进行倒序排序"""
        data.sort(key=lambda k: (k.get(key, 0)), reverse=True)
        return
        
    def get_top_data_of_world(self, n, key):
        """获取世界疫情某指标人数排名前n个国家"""
        data = self.get_last_day_data(KIND_WORLD)
        self._sort_by_key(data, key)
        return data[:n]
        
    def get_top_data_of_china(self, n, key):
        """获取全国疫情某指标人数排名前n个省份"""
        data = self.get_last_day_data(KIND_CHINA)
        self._sort_by_key(data, key)
        return data[:n]
    
    def get_area_data_of_china(self, areas):
        """获取中国某地区数据"""
        data = self.get_last_day_data(KIND_CHINA)
        data_map = {}
        for d in data:
            print(d)
            data_map[d.get('provinceShortName')] = {
                'confirmedCount': d.get('confirmedCount'),
                'curedCount': d.get('curedCount'),
                'deadCount': d.get('deadCount'),
            }
        return {area: data_map[area] for area in areas}
    
    def get_datedata_of_china_area(self, area):
        """获取某个省份的历史日期数据"""
        data = self.get_all_data(KIND_CHINA)
        data_map = {}
        for d in data:
            data_map[d.get('provinceName')] = d.get('data')
        return data_map[area]

    
    def get_datedata_of_world_country(self, country):
        """获取某个国家的历史日期数据"""
        data = self.get_all_data(KIND_WORLD)
        data_map = {}
        for d in data:
            data_map[d.get('provinceName')] = d.get('data')
        return data_map[country]
    