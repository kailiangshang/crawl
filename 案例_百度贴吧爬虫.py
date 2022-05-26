import requests
from lxml import etree
import pandas as pd


# 注意在爬取时可能会遇到网页无法读取的情况
# 对于一些浏览器引擎可能会将需要爬取的内容注释起来，解决有两个办法
# 1.采用更加低级的浏览器代理头
# 2.在爬取到数据之后，将注释起来的部分数据格式转换
# 一般来说第二种更加稳定

class TieBa:

    def __init__(self, name):
        self.url = f'https://tieba.baidu.com/f?kw={name}'
        self.headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 101.0.4951.64Safari / 537.36Edg / 101.0.1210.53',
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
        }

    def get_data(self, url):
        response = requests.get(url=url, headers=self.headers)
        with open('test.html', 'wb') as f:
            f.write(response.content)
        return response.content

    @staticmethod
    def parse_data(text):
        info_list = []
        html = etree.HTML(text)
        data_list = html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')[0]
        title_list = data_list.xpath('./@title')
        href_list = ['https://tieba.baidu.com' + href for href in data_list.xpath('./@href')]
        info_dict = {}
        for key, value in zip(title_list, href_list):
            info_dict[key] = value
            info_list.append(info_dict)
        try:
            new_url = 'https:' + html.xpath('//*[@id="frs_list_pager"]/a[last()-1]/@href')[0]
        except:
            new_url = None
        return info_list, new_url

    def run(self):
        new_url = self.url
        info_result = []
        while True:
            text = self.get_data(new_url)
            info_list, new_url = self.parse_data(text)
            info_result.append(info_list)
            if new_url is None:
                break
        return info_result


if __name__ == '__main__':
    tieba = TieBa('落俗')
    info = tieba.run()
    with open('result.txt', 'w') as f:
        f.write(str(info))
