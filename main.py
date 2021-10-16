import crawler
import storer
import viewer

from consts import KIND_WORLD, KIND_CHINA

def start_crawl(target_url):
    cr = crawler.Crawler(target_url)
    sr = storer.Storer()

    # 采集世界各国近一日数据
    last_day_data_of_world = cr.crawl_last_day_data_of_world()
    sr.set_last_day_data(KIND_WORLD, last_day_data_of_world)
    
    # # 采集中国各省近一日数据
    last_day_data_of_china = cr.crawl_last_day_data_of_china()
    sr.set_last_day_data(KIND_CHINA, last_day_data_of_china)
    
    # 采集世界各国历史数据
    all_data_of_world = cr.crawl_all_data_of_world(sr.get_last_day_data(KIND_WORLD))
    sr.set_all_data(KIND_WORLD, all_data_of_world)
    
    # 采集中国各省历史数据
    all_data_of_china = cr.crawl_all_data_of_china(sr.get_last_day_data(KIND_CHINA))
    sr.set_all_data(KIND_CHINA, all_data_of_china)
    return

def load_view():
    vr = viewer.Viewer()
    # 历史确诊人数top10国家
    #vr.top10_confirmed_of_world()
    # 历史确诊人数top10省份
    #vr.top10_confirmed_of_china()
    # 前一日确诊人数top10国家水平
    #vr.top10_last_day_confirmed_of_world()
    # 前一日确诊人数top10省份水平
    #vr.top10_last_day_confirmed_of_china()
    
    # 历史国内治愈人数热力图
    #vr.all_cured_of_china_by_heatmap()
    # 历史世界治愈人数热力图
    #vr.all_cured_of_world_by_heatmap()
    # 历史国内确诊人数热力图
    #vr.all_confirmed_of_china_by_heatmap()
    # 历史世界确诊人数热力图
    #vr.all_confirmed_of_world_by_heatmap()
    
    # 中国某省份 历史 确诊、死亡、治愈 人数条形图
    #vr.all_data_china_area()
    # 中国某地区各时间段疫情确诊/治愈人数折线图
    #vr.datedata_of_china_area()
    # 世界某国家各时间段疫情确诊/治愈人数折线图
    #vr.datedata_of_world_country()

if __name__ == '__main__':
    target_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
    #start_crawl(target_url)
    load_view()