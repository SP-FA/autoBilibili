import requests
import json
import http.cookiejar as cookielib
import re

class Bili:
    def __init__(self, uid):
        self.uid = uid;
        self.session = requests.session()
        self.session.cookies['DedeUserID'] = '277470241'
        self.session.cookies['DedeUserID__ckMd5'] = 'af579018a1a2b69b'
        self.session.cookies['SESSDATA'] = 'f658d72a%2C1660183655%2C20c26%2A21'
        self.session.cookies['bili_jct'] = '70e8a10f9998293cdb639fa52bacf3ab'
        self.session.cookies['LIVE_BUVID'] = 'AUTO8916133928311387'

        self.headers = {
            'origin': 'https://space.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
        }
        self.homePage = self.session.get('https://space.bilibili.com/%s/favlist' % uid, headers=self.headers)

    def verifyCookie(self):
        '''
        验证Cookie是否已登录
        返回值 errno：
            0 有效的 Cookie
            1 init 方法中未配置登录 Cookie
            2 无效的 Cookie
        '''
        if (self.session.cookies['DedeUserID'] == '' or self.session.cookies['DedeUserID__ckMd5'] == ''):
            return {'errno': 1, 'err_msg': '请在 init 方法中配置登录 Cookie'}
        else:
            home_page = self.homePage.content.decode("utf-8")
            if('个人空间_哔哩哔哩_Bilibili' in home_page):
                print(re.findall(r'<meta name="keywords" content="(.*),B站', home_page))
                user_name = re.findall(r'<meta name="keywords" content="(.*),B站', home_page)[0]
                return {'errno': 0, 'err_msg': '有效的Cookie，用户名：%s' % user_name}
            else:
                return {'errno': 2, 'err_msg': '无效的Cookie！'}

    def createFolder(self, name, intro="", privacy=0, cover=""):
        '''
        返回值 errno：
            0 运行成功
            1 运行失败
        '''
        url = r'https://api.bilibili.com/x/v3/fav/folder/add'
        data = {
            'title': name,
            'intro': intro,
            'privacy': 0,
            'cover': cover,
            'csrf': '70e8a10f9998293cdb639fa52bacf3ab',
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        print(check)
        if check['code'] == 0: # code = 0 运行成功
            return {'errno': 0, 'message': ""}
        else:
            return {'errno': 1, 'message': check['message']} 


if __name__ == '__main__':
    a = Bili('277470241')
    print(a.verifyCookie())
    print(a.createFolder('lxymyxdd', 'this is a test message'))