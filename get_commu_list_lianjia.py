import re
import os
import time
import pandas as pd

from main import  get_data,get_commu_info
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
(KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}

# 链家的爬小区列表, 全上海总共趴了三千多个小区, 因为在一百多页以后, 每页返回的数据是一样的
# https://sh.lianjia.com/xiaoqu/5011000012986/    这个网址可以查看小区的历史成交

def get_commu_ls_page(url):
    """获取小区列表"""
    print(url)
    res = pd.DataFrame()
    # 获取页码
    num = re.findall('.+pn(\d+)/',url)[0]
    # 获取网页文本
    res_elements, _ = get_data(url, headers)
    table = res_elements.xpath('//li[@class="clear xiaoquListItem"]')
    print(f'第{num}页'.center(60,'-'))
    for i, community in enumerate(table):
        print(time.strftime('%Y-%m-%d %H:%M:%S'),f'第{i + 1}个小区',end='')
        ss = etree.tostring(community, encoding='utf-8').decode()
        community = etree.HTML(ss)
        commu_code = community.xpath('//li[@class="clear xiaoquListItem"]/@data-id')[0]
        comm_url = f'https://sh.ke.com/api/listtop?type=resblock&resblock_id={commu_code}&source=ershou_xiaoqu'
        # 处理超时的情况
        try:
            commu_info = get_commu_info(comm_url,headers)
        except:
            print(f'小区编号{commu_code}请求超时...')
            continue
        # print(commu_info)
        name = commu_info['小区名称']
        print(f':{name}')
        res=res.append(commu_info,ignore_index=True)
        # if i>=2:
        #     break
    return res





def main():
    for num in range(726):
        # if num>=2:
        #     break
        try:
            url = f'https://sh.lianjia.com/xiaoqu/pg{num}/'
            df = get_commu_ls_page(url)
            df.to_csv(f'./result/第{num}页结果.csv',index=False)
        except:
            print(f'第{num}页出错了'.center(60,'!'))


def check():
    import os
    res=[]
    for name in os.listdir('./result'):
        pn  = re.findall('第(.+)页结果',name)[0]
        res.append(int(pn))

    for i in range(726):
        if i not in res:
            print(f"第{i}页不存在")
    print(sorted(res))



def check2():
    """将爬出来的结果union起来"""
    res = []
    for name in os.listdir('./result'):
        fname = os.path.join('./result',name)
        df_t = pd.read_csv(fname).iloc[:,1:]
        res.append(df_t)
    return  pd.concat(res,axis=0,ignore_index=True)


def get_index():
    url = 'https://www.anjuke.com/shanghai/cm/pudong/p28/'
    _,html_txt = get_data(url, headers)
    with open('./data/index.html','w') as f:
        f.write(html_txt)



if __name__ == "__main__":
    # main()
    # check()
    # get_commu_ls_page(680)
    # df = check2()
    # print(df.shape)
    # print(df.drop_duplicates().shape)
    # print(df[df['小区名称']=='新雅小区'])
    get_index()


# 第674页不存在
# 第677页不存在
# 第678页不存在
# 第679页不存在
# 第680页不存在


