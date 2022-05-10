import requests
import json
import http.cookiejar as cookielib
import re


class CookieException(Exception):
    '''
    ATTRIBUTE:
      @ msg: The error message
      @ errno: The error code
        0: Cookies are not configured in the init method
        1: invalid Cookie
    '''
    def __init__(self, err, msg):
        self.errno = err
        self.msg = msg

    def __str__(self):
        return "[Cookie error: %s] %s" % self.errno, self.msg


class FavlistException(Exception):
    '''
    ATTRIBUTE:
      @ msg: The error message
      @ errno: The error code
        0: The parameters are invalid
        1: Runtime Failures while creating folder
        2: Runtime Failures while deleting folder
        3: Runtime Failures while getting folders
        4: Can not find the folder
        5: Runtime Failures while getting the info of folder
        6: Runtime Failures while changing the info of folder
    '''
    def __init__(self, err, msg):
        self.errno = err
        self.msg = msg

    def __str__(self):
        return "[favlist error: %s] %s" % (self.errno, self.msg)


class BiliFavlist:
    def __init__(self, uid:str):
        self.uid = uid;
        self.session = requests.session()
        # You need to configure these cookies by yourself.
        self.session.cookies['DedeUserID'] = uid
        self.session.cookies['DedeUserID__ckMd5'] = 'af579018a1a2b69b'
        self.session.cookies['SESSDATA'] = 'f658d72a%2C1660183655%2C20c26%2A21'
        self.session.cookies['bili_jct'] = '70e8a10f9998293cdb639fa52bacf3ab'
        self.session.cookies['LIVE_BUVID'] = 'AUTO8916133928311387'

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
        homePage = self.session.get('https://space.bilibili.com/%s/favlist' % self.uid, headers=self.headers)
        if (self.session.cookies['DedeUserID'] == '' or self.session.cookies['DedeUserID__ckMd5'] == ''):
            raise CookieException(0, 'Please configure the Cookie in the init method')
        else:
            home_page = homePage.content.decode("utf-8")
            if ('个人空间_哔哩哔哩_Bilibili' not in home_page):
                raise CookieException(1, 'Invalid Cookie.')
            user_name = re.findall(r'<meta name="keywords" content="(.*),B站', home_page)[0]
            print('Valid Cookie, user name: %s' % user_name)


    def getFavlist(self) -> list:
        '''
        Get the favorite folder

        RETURN:
          a list of json data, which include the info of the favorite list

        EXCEPTION:
          FavlistException:
          @ errno 3: Runtime Failures while getting folders
        '''
        url = r'https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=' + self.uid
        check = self.session.get(url).json()
        if check['code'] != 0:
            raise FavlistException(3, check['message'])
        favList = check['data']['list']
        return favList


    def printFavlist(self, favList):
        '''
        Print the list of favorite folders
        '''
        print("\tid\t\tfid\t\ttitle\t\tmedia_count")
        for k, i in enumerate(favList):
            print('%s\t%10s\t%8s\t%s\t%s' % (k, i['id'], i['fid'], i['title'], i['media_count']))


    def checkFolder(self, mediaId):
        '''
        Check whether the folder is exist

        PARAMETER:
          @ mediaId: the folder id

        EXCEPTION:
          FavlistException:
          @ errno 4: Can not find the folder
        '''
        mediaList = self.getFavlist()
        for i in mediaList:
            if i['id'] == mediaId:
                return
        raise FavlistException(4, "Can not find the folder")


    def addFolder(self, name:str="", intro:str="", privacy:int=0, cover:str=""):
        '''
        Create a new folder

        PARAMETER:
          @ name: folder name
          @ intro: folder introduction
          @ privacy: 0 public, 1 private
          @ cover: cover image link

        EXCEPTION:
          FavlistException:
          @ errno 0: The parameters are invalid
          @ errno 1: Runtime Failures while creating folder
        '''
        if name == "":
            raise FavlistException(0, 'A folder name is needed.')
        if privacy != 0 and privacy != 1:
            raise FavlistException(0, 'Privacy must be 0 or 1.')
        url = r'https://api.bilibili.com/x/v3/fav/folder/add'
        data = {
            'title': name,
            'intro': intro,
            'privacy': privacy,
            'cover': cover,
            'csrf': '70e8a10f9998293cdb639fa52bacf3ab',
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0: # code = 0 运行成功
            raise FavlistException(1, check['message'])
        print('The folder has been created successfully.')


    def delFolder(self, mediaId:int):
        '''
        Delete a folder

        PARAMETER:
          @ mediaId: The id of the folder

        EXCEPTION:
          FavlistException:
          @ errno 0: The parameters are invalid
          @ errno 2: Runtime Failures while deleting folder
        '''
        try:
            self.checkFolder(mediaId)
        except FavlistException as fe:
            print(fe)
            return
        url = r'https://api.bilibili.com/x/v3/fav/folder/del'
        data = {
            "media_ids": mediaId,
            "platform": "web",
            "jsonp": "jsonp",
            "csrf": "70e8a10f9998293cdb639fa52bacf3ab",
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(3, check['message'])
        print('The folder has been deleted successfully.')


    def changeFolder(self, mediaId:int, title:str=None, intro:str=None, cover:str=None):
        '''
        change the information of the folder.

        PARAMETER:
          @ mediaId: the id of the folder.
          @ title: the new folder title.
          @ intro: the new intro of the folder.
          @ cover: the new cover.

        EXCEPTION:
          @ errno 6: Runtime Failures while changing the info of folder
        '''
        try:
            self.checkFolder(mediaId)
        except FavlistException as fe:
            print(fe)
            return
        url = r'https://api.bilibili.com/x/v3/fav/folder/edit'
        raw_data = self.getFolderInfo(mediaId)
        data = {
            "privacy": 0,
            "csrf": "70e8a10f9998293cdb639fa52bacf3ab",
            "media_id": mediaId,
        }
        data['title'] = raw_data['title'] if title == None else title
        data['intro'] = raw_data['intro'] if intro == None else intro
        data['cover'] = raw_data['cover'] if cover == None else cover
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(6, check['message'])
        print("The information has changed successfully.")


    def getFolderInfo(self, mediaId:int) -> json:
        '''
        get folders' info

        PARAMETER:
          @ mediaId: the id of the folder

        RETURN:
          a json contains the info

        EXCEPTION:
          FavlistException:
          @ errno 5: Runtime Failures while getting the info of the folder
        '''
        try:
            self.checkFolder(mediaId)
        except FavlistException as fe:
            print(fe)
            return
        url = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp' % mediaId
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FavlistException(5, check['message'])
        return check['data']['info']


    '''
    todo:
    排序
    对收藏的视频进行各种操作
    '''
    def sortFavlist(self):
        url = r'https://api.bilibili.com/x/v3/fav/folder/sort'
        favList = self.getFavlist()
        idList = []
        for i in favList:
            idList.append(i['id'])
        print(idList)
        pass


if __name__ == '__main__':
    a = BiliFavlist('277470241')
    # a.verifyCookie()
    # a.addFolder('lxymyxdd', 'this is a test message')
    # L = a.getFavlist()
    # a.printFavlist(L)
    # L = L[1 : 10]
    # for i in L:
    #     a.delFolder(i['id'])
    # a.getFolderInfo(1607747941)
    # a.changeFolder(1607747941, intro="sbwmyxdd", cover=r"https://wx2.sinaimg.cn/mw2000/005CgOGzly1h1yvun4oklj32jo1bmkjl.jpg")
    a.sortFavlist()