import time
import crawler
import storer
import viewer
import os
import webbrowser
import threading

from consts import KIND_WORLD, KIND_CHINA

target_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'

vr = viewer.Viewer()
cr = crawler.Crawler(target_url)
sr = storer.Storer()

def start_crawl():
    # 每次爬取前清空数据库，保证数据完整
    sr.reset_data()
    kinds = [KIND_WORLD, KIND_CHINA]
    
    # 采集近一日数据
    threads = []
    for kind in kinds:
        t = threading.Thread(target=_crawl_last_day_data, args=(kind, ))
        threads.append(t)
        t.start()
    # 等待所有线程任务结束
    for t in threads:
        t.join()
    
    # 采集历史数据（基于近一日数据进行爬取，所以不能和近一日爬取进行并发）
    threads = []
    for kind in kinds:
        t = threading.Thread(target=_crawl_all_data, args=(kind, ))
        threads.append(t)
        t.start()
    # 等待所有线程任务结束
    for t in threads:
        t.join()
    
        
    # # 采集世界各国近一日数据
    # last_day_data_of_world = cr.crawl_last_day_data_of_world()
    # sr.set_last_day_data(KIND_WORLD, last_day_data_of_world)
    
    # # # 采集中国各省近一日数据
    # last_day_data_of_china = cr.crawl_last_day_data_of_china()
    # sr.set_last_day_data(KIND_CHINA, last_day_data_of_china)
    
    # # 采集世界各国历史数据
    # all_data_of_world = cr.crawl_all_data_of_world(sr.get_last_day_data(KIND_WORLD))
    # sr.set_all_data(KIND_WORLD, all_data_of_world)
    
    # # 采集中国各省历史数据
    # all_data_of_china = cr.crawl_all_data_of_china(sr.get_last_day_data(KIND_CHINA))
    # sr.set_all_data(KIND_CHINA, all_data_of_china)
    return

 # 采集近一日数据
def _crawl_last_day_data(kind):
    if kind == KIND_WORLD:
        last_day_data = cr.crawl_last_day_data_of_world()
    elif kind == KIND_CHINA:
        last_day_data = cr.crawl_last_day_data_of_china()
    sr.set_last_day_data(kind, last_day_data)
    return

# 采集历史数据
def _crawl_all_data(kind):
    if kind == KIND_WORLD:
        all_data = cr.crawl_all_data_of_world(sr.get_last_day_data(KIND_WORLD))
    elif kind == KIND_CHINA:
        all_data = cr.crawl_all_data_of_china(sr.get_last_day_data(KIND_CHINA))
    sr.set_all_data(KIND_CHINA, all_data)
    return

def load_view(_id):
    if _id == 1:
        # 历史确诊人数top10国家
        vr.top10_confirmed_of_world()
    elif _id == 2:
        # 历史确诊人数top10省份
        vr.top10_confirmed_of_china()
    elif _id == 3:
        # 前一日确诊人数top10国家水平
        vr.top10_last_day_confirmed_of_world()
    elif _id == 4:
        # 前一日确诊人数top10省份水平
        vr.top10_last_day_confirmed_of_china()
    elif _id == 5:    
        # 历史国内治愈人数热力图
        fp = vr.all_cured_of_china_by_heatmap()
        webbrowser.open('file://' + os.path.join(os.getcwd(), fp))
    elif _id == 6:    
        # 历史世界治愈人数热力图
        fp = vr.all_cured_of_world_by_heatmap()
        webbrowser.open('file://' + os.path.join(os.getcwd(), fp))
    elif _id == 7:
        # 历史国内确诊人数热力图
        fp = vr.all_confirmed_of_china_by_heatmap()
        webbrowser.open('file://' + os.path.join(os.getcwd(), fp))
    elif _id == 8:
        # 历史世界确诊人数热力图
        fp = vr.all_confirmed_of_world_by_heatmap()
        webbrowser.open('file://' + os.path.join(os.getcwd(), fp))
    elif _id == 9:   
        # 中国某省份 历史 确诊、死亡、治愈 人数条形图
        vr.all_data_china_area()
    elif _id == 10:   
        # 中国某地区各时间段疫情确诊/治愈人数折线图
        vr.datedata_of_china_area()
    elif _id == 11:    
        # 世界某国家各时间段疫情确诊/治愈人数折线图
        vr.datedata_of_world_country()
    else:
        print("序号有误\n")

def menu():
    # 终端清屏
    os.system('cls')
    print("-------------------------------")
    print("|0.爬取疫情原始数据")
    print("|1.历史确诊人数top10国家柱状图")
    print("|2.历史确诊人数top10省份柱状图")
    print("|3.前一日确诊人数top10国家柱状图")
    print("|4.前一日确诊人数top10省份柱状图")
    print("|5.历史国内治愈人数热力图")
    print("|6.历史世界治愈人数热力图")
    print("|7.历史国内确诊人数热力图")
    print("|8.历史世界确诊人数热力图")
    print("|9.湖北省历史 确诊、死亡、治愈 人数条形图")
    print("|10.广东省各时间段疫情确诊/治愈人数折线图")
    print("|11.中国各时间段疫情确诊/治愈人数折线图")
    print("-------------------------------")
    _id = input("请输入序号：")
    return int(_id)

if __name__ == '__main__':
    while True:
        _id = menu()
        if _id == 0:
            print("* 开始数据爬取")
            start_t = time.time()
            start_crawl()
            end_t = time.time()
            print("* 完成数据爬取，耗时%ss" % int(end_t-start_t))
        else:
            load_view(_id)
        _ = input("任意数据继续>>>")
        