"""数据展示
# 世界各国 近一日 确诊人数 top 10 水平条形图
# 全国各省 近一日 确诊人数 top 10 水平条形图
# 世界各国 历史 确诊人数 top 10 水平条形图
# 全国各省 历史 确诊人数 top 10 水平条形图
# 全国各地 历史 确诊人数 热力图
# 全国各地 历史 治愈人数 热力图
# 世界各国 历史 治愈人数 热力图
# 世界各国 历史 确诊人数 热力图
# 中国某地区 历史确诊人数 省份 确诊、死亡、治愈 人数 条形图
# 中国历史各时间段疫情确诊\治愈 人数 折线图
# 中国历史各时间段疫情人数 折线图
# 广东历史各时间段疫情确诊人数 折线图
"""

import matplotlib.pyplot as plt
import matplotlib
import storer
import xlrd
from consts import KIND_WORLD, KIND_CHINA
import folium
from folium.plugins import HeatMap
import os


VIEWER_DATA_HANDLER = storer.DataHandler()


class BaseViewer():
    """基础类 提供基础方法"""
    
    def get_loction_of_china(self):
        """获取国内各城市经纬度"""
        # 读取xlsx内容
        book = xlrd.open_workbook('location/china.xlsx')
        # 使用第一个tab
        sheet = book.sheet_by_index(0)
        # 获取行数
        rows = sheet.nrows

        loc_map = {}
        for n in range(rows):
            row = sheet.row(n)
            area = row[0].value
            # 数据清洗
            if '市' not in area:
                continue
            loc = area.replace('市', '')
            loc_map[loc] = {
                'lon': row[2].value,
                'lat': row[1].value,
            }
        return loc_map
    
    def get_location_of_world(self):
        """获取世界各国经纬度"""
        # 读取xlsx内容
        book = xlrd.open_workbook('location/country.xlsx')
        # 使用第一个tab
        sheet = book.sheet_by_index(0)
        # 获取行数
        rows = sheet.nrows

        loc_map = {}
        for n in range(rows):
            row = sheet.row(n)
            loc_map[row[0].value] = {
                'lon': row[2].value,
                'lat': row[1].value,
            }
        return loc_map
    
    def get_format_for_last_day_data(self, raw):
        """获取格式化数据"""
        def _build_data(item):
            confirmed_count = item['confirmedCount']
            cured_count = item['curedCount']
            dead_count = item['deadCount']
            current_confirme_count = item['currentConfirmedCount']
            return {
                'confirmed_count': confirmed_count, # 历史确诊人数
                'cured_count': cured_count,         # 历史治愈人数
                'dead_count': dead_count,           # 历史死亡人数
                'current_confirme_count': current_confirme_count, # 当前确诊人数
            }
            
        data = {}
        for item in raw:
            tmp_data = _build_data(item)
            if 'cities' not in item:
                province_name = item['provinceShortName']
                if not province_name:
                    province_name = item['provinceName']
                data[province_name] = tmp_data
            else:
                cities = item['cities']
                for city in cities:
                    city_name = city['cityName']
                    data[city_name] = tmp_data
        return data

class Viewer(BaseViewer):
    def __init__(self):
        # 设置字体支持中文
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
    
    def _build_horizontal_histogram(self, data_map, title, xtitle):
        """绘制水平直方图
        
        Args：
            data_map (dict): 基础数据
            title (string): 正标题
            xtitle (string): x轴标题
        """

        keys = list(data_map.keys())
        vals = list(data_map.values())

        cnt = len(keys)
        plt.barh(range(cnt), vals, height=0.7, color='steelblue', alpha=0.8)      # 从下往上画
        plt.yticks(range(cnt), keys)
        plt.xlim(int(vals[len(vals)-1]/10), int(vals[0]*1.5))
        plt.xlabel(xtitle)
        plt.title(title)
        for x, y in enumerate(vals):
            plt.text(y + 0.2, x - 0.1, '%s' % y)
        plt.show()

    def top10_confirmed_of_world(self):
        """历史确诊人数top10国家水平直方图"""
        data = VIEWER_DATA_HANDLER.get_top_data_of_world(10, 'confirmedCount')        
        data_map = {}
        for d in data:
            # 国家
            provinceName = d['provinceName']
            # 确诊人数
            confirmedCount = d['confirmedCount']
            data_map[provinceName] = confirmedCount
        self._build_horizontal_histogram(data_map, '历史确诊人数top10国家', '历史确诊人数')
        
    def top10_confirmed_of_china(self):
        """历史确诊人数top10省份水平直方图"""
        data = VIEWER_DATA_HANDLER.get_top_data_of_china(10, 'confirmedCount')
        
        data_map = {}
        for d in data:
            # 省份
            provinceName = d['provinceName']
            # 确诊人数
            confirmedCount = d['confirmedCount']
            data_map[provinceName] = confirmedCount
        self._build_horizontal_histogram(data_map, '历史确诊人数top10省份', '历史确诊人数')
        
    def top10_last_day_confirmed_of_world(self):
        """前一日确诊人数top10国家水平直方图"""
        data = VIEWER_DATA_HANDLER.get_top_data_of_world(10, 'currentConfirmedCount')        
        data_map = {}
        for d in data:
            provinceName = d['provinceName']
            confirmedCount = d['currentConfirmedCount']
            data_map[provinceName] = confirmedCount
        self._build_horizontal_histogram(data_map, '昨日确诊人数top10国家', '昨日确诊人数')
        
    def top10_last_day_confirmed_of_china(self):
        """前一日确诊人数top10省份水平直方图"""
        data = VIEWER_DATA_HANDLER.get_top_data_of_china(10, 'currentConfirmedCount')
        
        data_map = {}
        for d in data:
            provinceName = d['provinceName']
            confirmedCount = d['currentConfirmedCount']
            data_map[provinceName] = confirmedCount
        self._build_horizontal_histogram(data_map, '昨日确诊人数top10省份', '昨日确诊人数')
        
    def _build_heatmap(self, kind, data, key, file_name):
        """构建热力图
                
        Args：
            kind (string): 类型 china or world
            data: 原始数据
            key (string): 根据key获取数值作为热力值
            file_path (string): 热力图存储文件名称
        """
        format_data = self.get_format_for_last_day_data(data)
        if kind == KIND_CHINA:
            loc_map = self.get_loction_of_china()
        else:
            loc_map = self.get_location_of_world()
            
        base_data = []
        for k, v in format_data.items():
            loc = loc_map.get(k) or None
            if not loc:
                continue
            # 获取经纬度
            lon, lat =  loc.get('lon'), loc.get('lat')
            # 根据key获取数值
            val = v.get(key)
            if not val or not lat or not lon:
                continue
            base_data.append([float(lat), float(lon), float(val)])

        # 设置热力图参数
        m = folium.Map(tiles='stamentoner', zoom_start=10)
        # 热力图生成
        HeatMap(base_data).add_to(m).show
        # 热力图保存
        m.save(os.path.join('heapmap', file_name))
        return
        
    def all_cured_of_china_by_heatmap(self):
        """历史国内治愈人数热力图"""
        kind = KIND_CHINA
        data = VIEWER_DATA_HANDLER.get_last_day_data(kind)
        self._build_heatmap(kind, data, 'cured_count','all_cured_of_china.html')
        return        
    
    def all_cured_of_world_by_heatmap(self):
        """历史世界治愈人数热力图"""
        kind = KIND_WORLD
        data = VIEWER_DATA_HANDLER.get_last_day_data(kind)
        self._build_heatmap(kind, data, 'cured_count','all_cured_of_world.html')
        return
    
    def all_confirmed_of_china_by_heatmap(self):
        """历史国内确诊人数热力图"""
        kind = KIND_CHINA
        data = VIEWER_DATA_HANDLER.get_last_day_data(kind)
        self._build_heatmap(kind, data, 'confirmed_count','all_confirmed_of_china.html')
        return    
    
    def all_confirmed_of_world_by_heatmap(self):
        """历史世界确诊人数热力图"""
        kind = KIND_WORLD
        data = VIEWER_DATA_HANDLER.get_last_day_data(kind)
        self._build_heatmap(kind, data, 'confirmed_count','all_confirmed_of_world.html')
        return
    
    def _build_multiple_horizontal_histogram(self, title, nums, xlabels):
        """绘制多类型水平直方图
        
        Args：
            title (string): 标题
            nums (list): 数值列表
            xlabels (list): 横坐标显示值
        """
        # 整理数值数据
        data = [[], [], []]
        for item in nums:
            data[0].append(item[0])
            data[1].append(item[1])
            data[2].append(item[2])
            
        # 确诊、死亡、治愈 共3种类型
        x = range(len(xlabels))
        confirmed = plt.bar(x=x, height=data[0], width=0.2, alpha=0.8, color='red', label="确诊")
        cured = plt.bar(x=[i + 0.2 for i in x], height=data[1], width=0.2, color='green', label="治愈")
        dead = plt.bar(x=[i + 0.4 for i in x], height=data[2], width=0.2, color='black', label="死亡")
        
        # 设置y轴取值范围
        plt.ylim(0, data[0][0] + int(data[0][0]/10) ) 
        plt.ylabel("人数")
        
        # 设置x轴刻度显示值
        plt.xticks([index + 0.2 for index in x], xlabels)
        
        plt.title(title) # 设置标题
        plt.legend()     # 设置题注
        
        # 编辑文本
        for item in confirmed:
            height = item.get_height()
            plt.text(item.get_x() + item.get_width() / 2, height+1, str(height), ha="center", va="bottom")
        for item in cured:
            height = item.get_height()
            plt.text(item.get_x() + item.get_width() / 2, height+1, str(height), ha="center", va="bottom")
        for item in dead:
            height = item.get_height()
            plt.text(item.get_x() + item.get_width() / 2, height+1, str(height), ha="center", va="bottom")
        plt.show()

    def all_data_china_area(self, areas=['湖北']):
        """中国某省份 历史确诊人数 省份 确诊、死亡、治愈 人数条形图"""
        data = VIEWER_DATA_HANDLER.get_area_data_of_china(areas)
        nums = []
        for area in areas:
            area_data = data[area]
            nums.append([area_data.get('confirmedCount'), area_data.get('curedCount'), area_data.get('deadCount')])
        self._build_multiple_horizontal_histogram('中国%s历史疫情情况人数分布' % areas[0] , nums, areas)
        return
    
    def _build_line_chart(self, title, date_vals, confirmed_vals, cured_vals, xlabel, ylabel):
        """构建折线图
        
        Args:
            xvals (list): x轴数值
            yvals (list): y轴数值
            xlabel: x轴标题
            ylabel: y轴标题
            title: 主标题
        """
        # 设置图标属性
        plt.plot(date_vals, confirmed_vals, ms=10, marker='*', label="确诊")
        plt.plot(date_vals, cured_vals, ms=10, marker='*', label="治愈")
        # x轴字体180度
        plt.xticks(rotation=90)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        # 将图例显示到左上角
        plt.legend(loc="upper left")
        plt.show()
        return
    
    def _get_fortmat_datedata(self, data):
        """构建折线图 X Y 坐标数据"""
        date_vals, confirmed_vals, cured_vals = [], [], []
        data_map = {}
        for d in data:
            # 去掉日期中的天，月为单位划分数据
            date = str(d.get('dateId'))[0:6]
            data_map[date] = [d.get('confirmedCount'), d.get('curedCount')]
        for k, v in data_map.items():
            date_vals.append(k) # 日期
            confirmed_vals.append(v[0])
            cured_vals.append(v[1])
        return date_vals, confirmed_vals, cured_vals
    
    def datedata_of_china_area(self, area='广东省'):
        """中国某地区各时间段疫情确诊/治愈人数折线图"""
        data = VIEWER_DATA_HANDLER.get_datedata_of_china_area(area)
        date_vals, confirmed_vals, cured_vals = self._get_fortmat_datedata(data)
        self._build_line_chart('%s疫情确诊人数折线图' % area, date_vals, confirmed_vals, cured_vals, '日期', '人数')
        
    def datedata_of_world_country(self, country='中国'):
        """世界某国家各时间段疫情确诊/治愈人数折线图"""
        data = VIEWER_DATA_HANDLER.get_datedata_of_world_country(country)
        date_vals, confirmed_vals, cured_vals = self._get_fortmat_datedata(data)
        self._build_line_chart('%s疫情治愈人数折线图' % country, date_vals, confirmed_vals, cured_vals, '日期', '人数')