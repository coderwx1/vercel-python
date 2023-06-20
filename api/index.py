from flask import Flask
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import random

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'About'


# ===================
# 测试ss api


# 随机生成一个 0 到 99 的整数作为 Chrome 版本号
version = f"{random.randint(1, 99)}.0.0.0"
userAgent = f'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36'

# email = input("\033[0;34m请输入邮箱地址：\033[0m")
email = 'freedomweb@yeah.net'


# 获取SS链接
def getSSLink(cookies):
    url = 'https://yypro.pro/user'
    headers = {
        "user-agent": userAgent,
        "referer": 'https://yypro.pro/user'
    }
    res = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    # 找到所有类名为"buttons"的元素
    buttons = soup.select('.buttons')
    # 获取第5个a标签
    fifth_a_tag = buttons[0].select('a')[4]
    # 获取"data-clipboard-text"属性的内容
    data_clipboard_text = fifth_a_tag['data-clipboard-text']
    return data_clipboard_text


# 购买
def buy(cookies):
    url = 'https://yypro.pro/user/buy'
    headers = {
        "user-agent": userAgent,
        "referer": 'https://yypro.pro/user'
    }
    params = {
        'coupon': '',
        'shop': 48,
        'autorenew': 0,
        'disableothers': 1
    }
    res = requests.post(url, params=params, cookies=cookies, headers=headers)

    if res.status_code == 200:
        data = res.json()
        print(f"\033[40;32m {data} \033[0m")
        sslink =  getSSLink(cookies)
        return sslink
    print(res.json(), res.status_code)


# 登陆
def login(eml):
    url = 'https://yypro.pro/auth/login'
    headers = {
        "user-agent": userAgent,
        "referer": 'https://yypro.pro/'
    }
    params = {
        'email': eml,
        'passwd': eml,
        'code': '',
        'remember_me': 'on'
    }
    res = requests.post(url, params=params, headers=headers)

    if res.status_code == 200:
        data = res.json()
        print(f"\033[40;32m {data} \033[0m")
        cookies = res.cookies.get_dict()
        # 将cookie保存到本地文件
        with open('cookie.json', 'w') as f:
            json.dump(cookies, f)
        sslink = buy(cookies)
        return sslink
    print(res.json(), res.status_code)


# 注册
@app.route('/register/<eml>/<captcha>')
def register(eml, captcha):
    url = 'https://yypro.pro/auth/register'
    headers = {
        "user-agent": userAgent,
        "referer": 'https://yypro.pro/'
    }
    params = {
        'email': eml,
        'name': eml,
        'passwd': eml,
        'repasswd': eml,
        'code': 0,
        'emailcode': captcha
    }
    res = requests.post(url, params=params, headers=headers)

    if res.status_code == 200:
        data = res.json()
        return data
    print(res.json(), res.status_code)


# 删除用户api
@app.route('/kill_user/<eml>')
def delateUser(eml):
    # login()
    # pwd = input('请输入您的密码：')
    url = 'https://yypro.pro/user/kill'
    headers = {
        "user-agent": userAgent,
        "referer": 'https://yypro.pro/user/profile'
    }
    params = {
      'passwd': eml
    }

    cookies = {}
    with open('cookie.json', 'r') as f:
        cookies = json.load(f)
    cookies['email'] = urllib.parse.unquote(cookies['email'])
    response = requests.post(url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    print('deluser===', response.json())


# 发送注册验证码
@app.route('/send_captcha/<eml>')
def sendCaptcha(eml):
    url = 'https://yypro.pro/auth/send'
    headers = {
        "user-agent": userAgent,
        "referer": 'https://yypro.pro/'
    }
    params = {
      'email': eml
    }
    response = requests.post(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['ret'] == 0:
            print(data)
            return data
        return data
    print(response.json(), response.status_code)


if __name__ == '__main__':
    app.run()
