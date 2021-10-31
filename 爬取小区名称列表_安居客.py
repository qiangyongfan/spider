import os

from main import  get_data
import joblib
import time
from lxml import etree
import numpy as np
import operator
from functools import reduce

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
(KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}




def get_commu_ls_ajk(url):
    """从安居客获取小区列表"""
    res_elements, _ = get_data(url, headers)
    table = res_elements.xpath('//ul[@class="P3"]')[0]
    ss = etree.tostring(table, encoding='utf-8').decode()
    table = etree.HTML(ss)
    table = table.xpath('//ul[@class="P3"]/li/em/a/text()')
    return table

def main():
    res = []
    for pn in range(100):
        url = f'https://www.anjuke.com/shanghai/cm/pudong/p{pn}/'
        ls = get_commu_ls_ajk(url)
        print(f"第{pn}页,获取到的小区名称列表{ls}")
        res.append(ls)
        time.sleep(1)
    # print(res)
    joblib.dump(res,'./data/安居客浦东小区名称列表')

def check_res():
    res = joblib.load('./data/安居客浦东小区名称列表')
    for i in range(1,101):
        print(f'前{i}行去重小区个数:',len(set(reduce(operator.add, res[:i]))))

def check_commu(commu_name):
    res = joblib.load('./data/安居客浦东小区名称列表')
    ls = set(reduce(operator.add, res))
    num_all= len(ls)
    if commu_name in ls:
        print(f'结果{num_all}个小区中包含小区名--->{commu_name}')
    else:
        print(f'结果{num_all}个小区中不包含小区名--->{commu_name}')




if __name__=="__main__":
    # main()
    # check_res()
    check_commu('环庆新苑')
# 环庆新苑 找不到, 还需要完善


