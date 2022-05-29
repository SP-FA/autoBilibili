from json import JSONDecodeError
from typing import *
import re


class UtilAcount:
    def __init__(self, path:str):
        try:
            with open(path) as f:
                cookie = json.load(f)

            self.uid = cookie['uid']
            self.session = requests.session()
            self.session.cookies['DedeUserID'] = self.uid
            self.session.cookies['DedeUserID__ckMd5'] = cookie['ckMd5']
            self.session.cookies['SESSDATA'] = cookie['SESSDATA']
            self.session.cookies['bili_jct'] = cookie['bili_jct']
            self.session.cookies['LIVE_BUVID'] = cookie['LIVE_BUVID']
        except (KeyError, JSONDecodeError):
            raise CookieException(0, 'Cookies are not configured in ' + path)

        self.headers = {
            'origin': 'https://space.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
        }


    def verifyCookie(self):
        '''
        Verify that Cookies are available
        
        EXCEPTION:
          CookieException
          @ errno 0: invalid Cookie
          @ errno 1: Cookies are not configured in the init method correctly
        '''
        url = 'https://space.bilibili.com/%s/favlist' % self.uid
        homePage = self.session.get(url, headers=self.headers)
        home_page = homePage.content.decode("utf-8")
        if ('个人空间_哔哩哔哩_Bilibili' not in home_page):
            raise CookieException(1, 'Invalid Cookie.')
        user_name = re.findall(r'<meta name="keywords" content="(.*),B站', home_page)[0]
        print('Valid Cookie, user name: %s' % user_name)


if __name__ == "__main__":
    test = UtilAcount("cookies.json")
    test.verifyCookie()