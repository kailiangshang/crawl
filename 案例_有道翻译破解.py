import requests
import hashlib
import time
import random
import json


class YOU_dao:

    def __init__(self, word: str):
        self.url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
            'Cookie': '_ga=GA1.2.70194764.1653981376;OUTFOX_SEARCH_USER_ID_NCOO=1140302600.1656175; OUTFOX_SEARCH_USER_ID="-1288328574@10.110.96.158";fanyi-ad-id=306808; fanyi-ad-closed=1; ___rl__test__cookies=1655169474769',
            'Referer': 'https://fanyi.youdao.com/'
        }
        self.word = word
        self.info_data = self.get_info_data()

    def get_info_data(self) -> dict:
        """
        :return: 请求表单
        """
        ts = str(int(time.time()*1000))  # 时间戳

        salt = ts + str(random.randint(0, 9))

        # hash加密
        temp_str = "fanyideskweb" + self.word + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        md5 = hashlib.md5()
        md5.update(temp_str.encode())
        sign = md5.hexdigest()

        info_data = {
            'i': self.word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': ts,
            'bv': 'edd43abc5f8038d69864db1ea7a752d9',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        return info_data

    def get_data(self) -> json:
        """
        :return: 翻译响应内容
        """
        response = requests.post(self.url, data=self.info_data, headers=self.headers)
        return response.content

    def parse_data(self) -> str:
        """
        :return: 解析后的翻译结果
        """
        result_dict = json.loads(self.get_data())
        return result_dict['translateResult'][0][0]['tgt']

    def run(self):
        return self.parse_data()


if __name__ == '__main__':
    youdao = YOU_dao('what')
    print(youdao.run())



















