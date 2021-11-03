import pandas as pd

from main import  get_data,get_commu_info,headers
from lxml import etree
import re
from get_commu_list_lianjia import  get_commu_ls_page

# 安居客根据更细致的细分区域获取更完整的小区列表

# 获取浦东的板块名称列表
def get_bankuai_info(url):
    """拿到一个区的url,获取这个区的细分板块名称和url"""
    res_elements, _ = get_data(url, headers)
    urls = res_elements.xpath('//div[@class="position"]/dl[last()]/dd/div/div[last()]/a/@href')
    names = res_elements.xpath('//div[@class="position"]/dl[last()]/dd/div/div[last()]/a/text()')

    res = {}
    for name,url in zip(names,urls):
        res[name] = 'https://sh.ke.com' + url
    return res


def get_commu_num(url):
    """拿到板块对应的url后,获取该板块下有多少小区,以均订有多少页"""
    res_elements, res_text = get_data(url, headers)
    # print(res_text)
    ss = res_elements.xpath('//div[@data-component="listOverview"]/h2/span')[0]
    commu_num = etree.tostring(ss, encoding='utf-8').decode()
    commu_num = re.findall('.*<span>(.+)</span>.*',commu_num)[0].strip()
    return int(commu_num)

def get_comm_ls_pg(pg_url):
    """获取一页中所有的小区名称和信息"""
    res = []
    res_elements, res_text = get_data(pg_url, headers)
    commu_names = res_elements.xpath('//ul[@class="listContent"]/li/a/@title')
    urls = res_elements.xpath('//ul[@class="listContent"]/li/a/@href')
    response_ids = res_elements.xpath('//ul[@class="listContent"]/li/@data-id')
    for commu_info in zip(commu_names,response_ids,urls):
        res.append(list(commu_info))

    df_res = pd.DataFrame(res,columns=['小区名称','response_id','url'])
    return df_res

def get_commu_ls_region(url,name_qu):
    res_df = pd.DataFrame()
    # 获取浦东的板块名
    bankuai_dic = get_bankuai_info(url)
    print(bankuai_dic)
    # 循环获取每个板块的小区名称
    for name, url in bankuai_dic.items():
        # 获取该板块的小区数
        commu_num = get_commu_num(url)
        print(f"{name}板块共有{commu_num}个小区".center(80, '-'))
        pg_nums = int(commu_num / 30) + 2

        # 循环获取该板块的所有小区
        for pg_num in range(1, pg_nums):
            pg_url = url + f'pg{pg_num}/'
            print(pg_url)
            # 获取一个页面的小区列表
            n=0
            while n<=10:
                try:
                    commus_pg_df = get_comm_ls_pg(pg_url)
                except:
                    n+=1
                break
            if n==11:
                continue

            commus_pg_df['板块名称'] = name
            res_df = res_df.append(commus_pg_df)
            print(f"目前已拿到{res_df.shape[0]}个小区")
    res_df['区名'] = name_qu
    res_df.to_csv(f'./data/{name_qu}小区列表.csv',index=False)
    return res_df


def get_region_info():
    """获取上海所有区的区名和对应url"""
    url = 'https://sh.ke.com/xiaoqu/'
    res = {}
    res_elements, res_text = get_data(url, headers)
    region_names = res_elements.xpath('//div[@data-role="ershoufang"]/div/a/text()')[:-1]
    urls = res_elements.xpath('//div[@data-role="ershoufang"]/div/a/@href')[:-1]
    # ss = etree.tostring(ss, encoding='utf-8').decode()
    print(region_names)
    print(urls)
    for name,url in zip(region_names,urls):
        res[name] = 'https://sh.ke.com'+url
    return res


if __name__=="__main__":
    # url = 'https://sh.ke.com/xiaoqu/pudong/'
    # get_commu_ls_region(url)
    # 获取区名和对应的url
    # res_df = pd.DataFrame()
    # regions = get_region_info()
    # for name_qu , url_qu in regions.items():
    #     print(f'正在获取{name_qu}的小区名称'.center(90,'*'))
    #     df_qu = get_commu_ls_region(url_qu,name_qu)
    #     res_df = res_df.append(df_qu)
    # res_df.to_csv('./data/上海市小区名称列表_链家.csv',index=False)
    import os
    ls =[]
    for name in os.listdir('./data'):
        if re.findall('.*小区列表.*',name):
            name = os.path.join('./data',name)
            df_t = pd.read_csv(name)
            ls.append(df_t)
    df = pd.concat(ls,axis=0,ignore_index=True)
    print(df.head())
    df.to_csv('./data/上海市小区名称列表_链家.csv',index=False,encoding='utf8')
    df.to_excel('./data/上海市小区名称列表_链家.xlsx', index=False)














