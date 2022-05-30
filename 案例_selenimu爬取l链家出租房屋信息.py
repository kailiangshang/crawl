import time
import numpy as np
import pandas as pd
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver


class get_lianjia_info:

    def __init__(self):
        self.url = 'https://bd.lianjia.com/zufang/'
        self.service = self.s = Service(executable_path='D:/edgedriver_win64/msedgedriver.exe')
        self.driver = webdriver.Edge(service=self.service)

    def open_edge(self):
        self.driver.get(self.url)

    @staticmethod
    def open_next_edge(driver):
        """
        :param driver: 当前window下的driver
        :return: None
        """
        # 将页面下滑到页面最下端
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_window = driver.find_element(by=By.LINK_TEXT, value='下一页')
        next_window.click()

    @staticmethod
    def get_info(driver):
        """
        :param driver: 当前页面元素
        :return: 当前页面的信息
        """
        info_df_now = pd.DataFrame(columns=['text', 'price'])
        text = driver.find_elements(by=By.XPATH, value='//*[@id="content"]/div[1]/div[1]/div/div/p[1]/a')
        text = [i.text for i in text]
        price = driver.find_elements(by=By.XPATH, value='//*[@id="content"]/div[1]/div[1]/div/div/span/em')
        price = [int(i.text) for i in price]
        info_df_now['text'] = text
        info_df_now['price'] = price
        return info_df_now

    def run(self):
        # 打开58同城某个租房信息首页
        self.open_edge()

        # 初始化打开首页
        driver_now = self.driver

        # 初始化总信息
        info_df_sum = pd.DataFrame(columns=['text', 'price'])

        while True:
            try:

                # 获取该页的所有信息
                info_df_now = self.get_info(driver_now)
                info_df_sum = pd.concat([info_df_sum, info_df_now], ignore_index=True)

                # 关闭当前页
                # driver_now.close()
                time.sleep(3)

                # 点击下一页
                self.open_next_edge(driver_now)

                # 获取当前浏览器窗口列表，将driver定位到最新打开的标签页
                windows_list = driver_now.window_handles
                driver_now.switch_to.window(windows_list[-1])

            except:
                driver_now.quit()
                break
        return info_df_sum


if __name__ == '__main__':
    get_58 = get_lianjia_info()
    get_58.run().to_csv('lianjia.csv')
