import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from lxml import etree
import time


class get_58_info:
    def __init__(self):
        self.url = 'https://bd.58.com/chuzu/pn1/'
        self.s = Service(executable_path='D:/edgedriver_win64/msedgedriver.exe')
        self.driver = webdriver.Edge(service=self.s)

    def open_page(self, url):
        """
        :param url: 地址
        :return: 页面打开
        """
        self.driver.get(url)

    def get_info(self):
        """
        :return: 当前页面的页面信息
        """
        page_info = self.driver.page_source
        html = etree.HTML(page_info)
        text = html.xpath('/html/body/div[6]/div[2]/ul/li/div[2]/h2/a/text()')
        price = html.xpath('/html/body/div[6]/div[2]/ul/li/div[3]/div[2]/b/text()')
        try:
            next_url = html.xpath('//*[@id="pager_wrap"]/div/a[last()]/@href')[0]
        except:
            self.driver.quit()
            next_url = None
        info_df = pd.DataFrame(columns=['text', 'price'])
        info_df['text'] = text
        info_df['price'] = price
        return info_df, next_url

    # def next_page(self):
    #     try:
    #         self.driver.find_element(by=By.CLASS_NAME, value='next').click()
    #         # result = 0
    #         # return result
    #     except:
    #         self.driver.quit()
    #         # result = 1
    #         # return result

    def run(self):
        # 打开保定58租房网站
        url = self.url

        # 初始化信息
        info_df = pd.DataFrame(columns=['text', 'price'])

        # 判断是否为最后一页
        while True:
            self.open_page(url)
            info_df_now, url = self.get_info()
            # 获取租房的标题和每月费用的信息, 并写入表格
            info_df = pd.concat([info_df, info_df_now], ignore_index=True)

            # 当前页面信息存储完毕后退出浏览器
            self.driver.close()

            # 将已有的信息写入csv文件中，防止反爬机制下导致页面无法点击，信息丢失
            # info_df.to_csv('info.csv')

            # 为了最大限度防止页面无法访问，获取当前页面信息后，停止随机秒数
            # time.sleep(np.random.randint(10, 20))


if __name__ == '__main__':
    get = get_58_info()
    get.run()














