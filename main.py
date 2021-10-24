import pandas as pd
import numpy as np
from lxml import etree
import requests
import re
# 设置展示的最大宽度
desired_width = 3200
pd.set_option('display.width', desired_width)
# 显示的最大列数，解决中间被省略为...的问题
pd.set_option("display.max_columns",None)
# 将标题和数据左对齐,默认右对齐
pd.set_option('colheader_justify', 'left')
import warnings
warnings.filterwarnings('ignore')

def get_data(addr_name):
    """获取指定url的数据, 并将结果新增city字段
       url:数据地址
       city:改地址的城市名称
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
    (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
    url = f'https://sh.lianjia.com/ershoufang/rs{addr_name}/'
    res = requests.get(url, headers=headers)
    # print(res.text)
    res_elements = etree.HTML(res.text)
    return res_elements


def get_house_num(res_elements):
    """获取小区在售的二手房套数"""
    table = res_elements.xpath('//h2[@class="total fl"]/span')
    ss = etree.tostring(table[0], encoding='utf-8').decode()
    num =re.findall('<span>(.+?)</span>.*',ss)[0].strip()
    return num

def get_house_info(res_elements):
    """获取在售的房子信息, 包括所属板块,几室几厅,面积, 售价"""

    def create_ser(columns,num):
        house_res = pd.Series(index=columns)
        house_res['在售套数'] = num
        return house_res
    # 存储结果用的DataFrame
    columns = ['在售套数', 'title', '板块名称', '小区名称', '室厅', '面积', '卧室朝向', '装修', '楼层', '年份', '类型', '总价', '单价']
    res = pd.DataFrame(columns=columns)

    # 获取该小区在售的房屋套数
    num = get_house_num(res_elements)
    print(f'{addr_name} 共有{num}套二手房在售')

    # 获取在售房屋列表
    table = res_elements.xpath('//div[@class="info clear"]')
    print('-' * 60)

    # 如果在售为0套, 新建一个空的Series, 包含在售的套数
    if int(num)==0:
        house_res = create_ser(columns, num)
        res = res.append(house_res,ignore_index=True)
    else:
        # 提取在售房屋的信息
        for i,houss in enumerate(table):
            house_res = create_ser(columns, num)
            print(f'第{i+1}套')
            # 将选出来得条目转成text, 再转成网页树
            ss = etree.tostring(houss,encoding='utf-8').decode()
            houss = etree.HTML(ss)

            # 提取房子信息
            # 标题
            title = houss.xpath('//div[@class="title"]/a[@class="LOGCLICKDATA "]/text()')[0]
            print(f"title:{title}")
            house_res['title'] = title

            # 板块
            region_name = houss.xpath('//div[@class="positionInfo"]/a/text()')
            print(f"板块名称:{region_name}")
            house_res['板块名称'] = region_name[1]
            house_res['小区名称'] = region_name[0]

            # 房屋信息
            house_info = houss.xpath('//div[@class="houseInfo"]/text()')[0]
            print(f"房屋信息:{house_info}")
            house_res['室厅'] = house_info.split('|')[0]
            house_res['面积'] = house_info.split('|')[1]
            house_res['卧室朝向'] = house_info.split('|')[2]
            house_res['装修'] = house_info.split('|')[3]
            house_res['楼层'] = house_info.split('|')[4]
            house_res['年份'] = house_info.split('|')[5]
            house_res['类型'] = house_info.split('|')[6]

            # 价格
            price = houss.xpath('//div[@class="priceInfo"]/div[@class="totalPrice totalPrice2"]')[0].xpath('string(.)')
            print(f'总价:{price}')
            house_res['总价'] = price

            # 单价
            unit_price = houss.xpath('//div[@class="priceInfo"]/div[@class="unitPrice"]')[0].xpath('string(.)')
            print(f"单价:{unit_price}")
            house_res['单价'] = unit_price

            print('-'*60)
            res = res.append(house_res,ignore_index=True)
    return res


addr_names = ['金领国际','龚路新村','龚华公寓','龚路新城']
res = []
for addr_name in addr_names :
    # 获取网页
    res_elements = get_data(addr_name)

    # 获取二手房的信息
    res_df = get_house_info(res_elements)
    res.append(res_df)
result = pd.concat(res,axis=0)
print(result)

