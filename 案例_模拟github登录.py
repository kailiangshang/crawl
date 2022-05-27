import requests
import re
# commit: Sign in
# authenticity_token: T_yFBcIeJj-nj0mIeG7ZXBWWPj5qGdxS8IjtQ9Eec4W_aE-J5Cyq-weJAcXTW08Cepmshgp3hKWMztAL1srm1g
# trusted_device:
# webauthn-support: supported
# webauthn-iuvpaa-support: unsupported
# return_to: https://github.com/login
# allow_signup:
# client_id:
# integration:
# required_field_e5b0:
# timestamp: 1653188781451
# timestamp_secret: 123b9f76978e0ab28e944e17b3e9e3d4a8e4fa59819a1b534b6a66ab5391b1b3

# <input type="text" name="required_field_b485" hidden="hidden" class="form-control" /><input type="hidden"
# name="timestamp" value="1653189391000" autocomplete="off" class="form-control" /><input type="hidden"
# name="timestamp_secret" value="b9e398dfdfddea32577cfa4e2123ee98d5afb75cc4e9054bbac8a1686b3fc7c7" autocomplete="off"
# class="form-control" /> <!-- '"` --><!-- </textarea></xmp> --></option></form><form data-turbo="false"
# action="/session" accept-charset="UTF-8" method="post"><input type="hidden" name="authenticity_token"
# value="uAjBTGh5sd4FXMtklTt03Oa_whr99CgLab0JAYF6vfdoAQ2qcXNkyw3wQoZ7YUpqsusFEHscpMG5jsjoCap14Q" />  <label
# for="login_field">


def login():
    """
    1.url1 获取响应，并获得表单信息，利用session保持状态
    2.url2 传入表单信息，模拟登录
    3.url3 验证登录是否成功
    """
    url1 = 'https://github.com/login'
    session = requests.session()
    session.headers = {
        'user - agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 101.0.4951.64afari / 537.36Edg / 101.0.1210.53'
    }
    res1 = session.get(url1).content.decode()
    token = re.findall(r'name="authenticity_token" value="(.*?)" />', res1)[0]
    timestamp = re.findall(r'name="timestamp" value="(.*?)"', res1)[0]
    time_secret = re.findall(r'name="timestamp_secret" value="(.*?)"', res1)[0]

    data = {
        'commit': 'Sign in',
        'authenticity_token': token,
        'login': '1972475358 @ qq.com',
        'password': 'woshengri826',
        'trusted_device': '',
        'webauthn-support': 'supported',
        'webauthn-iuvpaa-support': 'unsupported',
        'return_to': 'https://github.com/login',
        'allow_signup': '',
        'client_id': '',
        'integration': '',
        'required_field_e5b0': '',
        'timestamp': timestamp,
        'timestamp_secret': time_secret
    }

    url2 = 'https://github.com/session'
    session.post(url2, data)

    url3 = 'https://github.com/kailiangshang'
    res3 = session.get(url3)
    with open('github.html', 'wb') as f:
        f.write(res3.content)


if __name__ == '__main__':
    login()






