from main import  get_data,get_commu_info,headers
from lxml import etree
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
        # print(f'{name}:https://sh.ke.com{url}')
        res[name] = 'https://sh.ke.com' + url
    return res




if __name__=="__main__":
    url = 'https://sh.ke.com/xiaoqu/pudong/'
    bankuai_dic = get_bankuai_info(url)
    print(bankuai_dic)
    for name,url in bankuai_dic.items():
        print(url)
        for pn in range(1,10):
            # 获取小区列表
            # print(get_commu_ls_page(url+f'pn{pn}/'))
        break







