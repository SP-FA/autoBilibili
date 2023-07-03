import requests
from json import JSONDecodeError
import json
import re
from _exception import CookieException, ExceptionEnum


class UtilAccount:
    def __init__(self, path: str):
        try:
            with open(path) as f:
                cookie = json.load(f)

            self.uid = cookie['uid']
            self.session = requests.session()
            self.session.cookies['DedeUserID'] = self.uid
            self.session.cookies['DedeUserID__ckMd5'] = cookie['ckMd5']
            self.session.cookies['Expires'] = cookie['Expires']
            self.session.cookies['SESSDATA'] = cookie['SESSDATA']
            self.session.cookies['bili_jct'] = cookie['bili_jct']
            self.session.cookies['LIVE_BUVID'] = cookie['LIVE_BUVID']

        except (KeyError, JSONDecodeError):
            raise CookieException(ExceptionEnum.COOKIE_CONFIG_ERR, 'Cookies are not configured in ' + path)

        self.headers = {
            'origin': 'https://space.bilibili.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/39.0.2171.95 Safari/537.36"
        }

    def verify_cookie(self):
        """
        Verify that Cookies are available

        EXCEPTION:
          CookieException
          @ errno 0: invalid Cookie
          @ errno 1: Cookies are not configured in the init method correctly
        """
        url = 'https://space.bilibili.com/%s/favlist' % self.uid
        homePage = self.session.get(url, headers=self.headers)
        home_page = homePage.content.decode("utf-8")
        if '个人空间' not in home_page:
            raise CookieException(ExceptionEnum.INVALID_COOKIE_ERR, 'Invalid Cookie.')
        user_name = re.findall(r'关注(.*)账号，第一时间了解UP注动态。', home_page)[0]
        print('Valid Cookie, user name: %s' % user_name)


if __name__ == "__main__":
    test = UtilAccount("../cookies.json")
    test.verify_cookie()
