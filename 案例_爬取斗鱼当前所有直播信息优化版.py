import time
import pandas as pd
from lxml import etree
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By


class DouYu_crawl:

    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'  # url地址
        self.service = Service(executable_path='D:/edgedriver_win64/msedgedriver.exe')  # 浏览器驱动
        self._option = webdriver.EdgeOptions()
        self._option.add_argument('headless')
        self.driver = webdriver.Edge(service=self.service, options=self._option)
        self._wait_time = 3

    def get_page_source(self):
        """
        :return: 当前页面总信息获取
        """
        html = self.driver.page_source
        return etree.HTML(html)

    @staticmethod
    def parse_data(html):
        """
        :param html: 传入当前页面的源代码
        :return: 信息表
        """
        info_df = pd.DataFrame(columns=['分类', '主播', '热度'])
        info_df['分类'] = html.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[2]/h2/div/text()')
        info_df['主播'] = html.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[2]/h2/div/text()')
        info_df['热度'] = html.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[2]/span/text()')
        return info_df

    def open_next_page(self):
        self.driver.execute_script('scrollTo(1000, document.body.scrollHeight)')
        el = self.driver.find_element(by=By.XPATH, value='//*[@id="listAll"]/section[2]/div[2]/div/ul/li[last()]/span')
        el.click()

    def run(self):
        # 初始化请求参数（无头浏览，加快速度，隐式等待时间设置）
        self.driver.get(self.url)
        # 注意这个时间设置是十分关键的，因为在打开页面后有侧面弹框，如果不等待，会导致后续操作无法进行
        time.sleep(5)
        info_df_sum = pd.DataFrame(columns=['分类', '主播', '热度'])
        info_df_now = pd.DataFrame(columns=['分类', '主播', '热度'])
        i = 0
        while True:
            # selenimu获取当前页html信息
            html = self.get_page_source()
            if info_df_now.equals(self.parse_data(html)) is True:
                self.driver.quit()
                break

            else:
                # etree模块解析当前页数据parse，并将其存入df中
                info_df_now = self.parse_data(html=html)
                info_df_sum = pd.concat([info_df_sum, info_df_now], ignore_index=True)
                i += 1
                print('当前页信息统计完成', i)

                # 鼠标滚轮下滑,并点击下一页
                self.open_next_page()
        return info_df_sum


if __name__ == '__main__':
    t_start = time.time()
    douyu = DouYu_crawl()
    douyu.run().to_csv('douyu.csv')
    t_end = time.time()
    print(t_end-t_start)










