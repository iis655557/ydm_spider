"""
思路：
1. 获取验证码图片；
2. 将这个验证码图片保存到本地，同时将这个图片上传至云打码平台进行识别；
3. 将云打码识别的结果和登录的其它参数拼接成url，发送请求进行登录，获取登录结果；
"""

from ydm import YDMHttp
from http.cookiejar import LWPCookieJar
import requests, json

class YDMLoginSpdier(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.cookies = LWPCookieJar(filename='zhihu.txt')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }

    def login(self):
        # 1. 获取验证码图片内容，并保存至本地
        content = self.session.get(url='http://www.yundama.com/index/captcha', headers=self.headers).content
        with open('captcha.png', 'wb') as f:
            f.write(content)

        # 2. 开始调用云打码，进行在线识别
        # username和password是普通用户的账号密码
        ydm_obj = YDMHttp(username='', password='', appid=5103, appkey='74598e8ff5b463663a8bb5480911184e')
        cid, result = ydm_obj.decode(filename='captcha.png', codetype=3000, timeout=60)

        # 3. 开始登录
        login_url = 'http://www.yundama.com/index/login?username=gaodeveloper&password=gao12345&utype=2&vcode={}'.format(result)
        json_dict = json.loads(self.session.get(url=login_url, headers=self.headers).text)
        print('登录结果是：', json_dict['msg'])


if __name__ == '__main__':
    obj = YDMLoginSpdier()
    obj.login()


