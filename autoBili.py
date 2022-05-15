import requests
import json
import http.cookiejar as cookielib
import re
from typing import *

 
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
        3: Runtime Failures while getting favlist
        4: Can not find the folder
        5: Runtime Failures while getting the info of folder
        6: Runtime Failures while changing the info of folder
        7: Runtime Failures while moving folders
    '''
    def __init__(self, err, msg):
        self.errno = err
        self.msg = msg

    def __str__(self):
        return "[favlist error: %s] %s" % (self.errno, self.msg)


class BiliFavlist:
    def __init__(self): # uid:int
        self.uid = str(277470241)# str(uid);
        self.session = requests.session()
        # You need to configure these cookies by yourself.
        self.session.cookies['DedeUserID'] = self.uid
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
        url = 'https://space.bilibili.com/%s/favlist' % self.uid
        homePage = self.session.get(url, headers=self.headers)
        if (self.session.cookies['DedeUserID'] == '' or self.session.cookies['DedeUserID__ckMd5'] == ''):
            raise CookieException(0, 'Please configure the Cookie in the init method')
        else:
            home_page = homePage.content.decode("utf-8")
            if ('个人空间_哔哩哔哩_Bilibili' not in home_page):
                raise CookieException(1, 'Invalid Cookie.')
            user_name = re.findall(r'<meta name="keywords" content="(.*),B站', home_page)[0]
            print('Valid Cookie, user name: %s' % user_name)


    def getFavlist(self) -> List[Dict]:
        '''
        Get the favorite folder

        RETURN:
          a list of json data, which include the info of the favorite list

        EXCEPTION:
          FavlistException:
          @ errno 3: Runtime Failures while getting folders
        '''
        url = r'https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=' + self.uid
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FavlistException(3, check['message'])
        favList = check['data']['list']
        return favList



    def printFavlist(self, favList:List[Dict]):
        '''
        Print the list of favorite folders

        PARAMETER:
          @ favList: folder list, and the element is the dict of the info of each folder.
        '''
        print("\tid\t\tfid\t\ttitle\t\tmedia_count")
        for k, i in enumerate(favList):
            print('%s\t%10s\t%8s\t%s\t%s' % (k, i['id'], i['fid'], i['title'], i['media_count']))


    def checkFolder(self, mediaId:int):
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


    def delFolder(self, mediaId:int):
        '''
        Delete a folder

        PARAMETER:
          @ mediaId: The id of the folder

        EXCEPTION:
          FavlistException:
          @ errno 0: The parameters are invalid
          @ errno 2: Runtime Failures while deleting folder
          @ errno 4: Can not find the folder
        '''
        self.checkFolder(mediaId)
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


    def changeFolder(self, mediaId:int, title:str=None, intro:str=None, cover:str=None):
        '''
        change the information of the folder.

        PARAMETER:
          @ mediaId: the id of the folder.
          @ title: the new folder title.
          @ intro: the new intro of the folder.
          @ cover: the new cover.

        EXCEPTION:
          @ errno 4: Can not find the folder
          @ errno 5: Runtime Failures while getting the info of the folder
          @ errno 6: Runtime Failures while changing the info of folder
        '''
        raw_data = self.getFolderInfo(mediaId)
        url = r'https://api.bilibili.com/x/v3/fav/folder/edit'
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


    def getFolderInfo(self, mediaId:int) -> Dict:
        '''
        get folders' info

        PARAMETER:
          @ mediaId: the id of the folder

        RETURN:
          a json contains the info

        EXCEPTION:
          FavlistException:
          @ errno 4: Can not find the folder
          @ errno 5: Runtime Failures while getting the info of the folder
        '''
        self.checkFolder(mediaId)    
        url = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp' % mediaId
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FavlistException(5, check['message'])
        keys = ['id', 'fid', 'title', 'cover', 'cnt_info', 'intro', 'media_count']
        check = check['data']['info']
        info = {}
        for i in keys:
            info[i] = check[i]
        return info


    def moveFolder2(self, mediaId:int, index:int):
        '''
        Move a folder to index, index = 0 is the default favorites folder,
        so index must at least 1 in this method. 

        PARAMETER:
          @ mediaId: the folder id you want to move.
          @ index: the index you want to move to.

        EXCEPTION:
          FavlistException:
          @ errno 4: Can not find the folder
          @ errno 7: Runtime Failures while moving folders
        '''
        self.checkFolder(mediaId)
        if index == 0:
            raise FavlistException(0, "index can not be 0, it must at least 1")

        url = r'https://api.bilibili.com/x/v3/fav/folder/sort'
        favList = self.getFavlist()
        idList = []
        for i in favList:
            idList.append(i['id'])
        idList.remove(mediaId)
        try:
            idList.insert(index, mediaId)
        except IndexError as ie:
            idList.append(mediaId)
            print("Index out of range, it will be moved to the bottom of the list")

        idstr = ""
        for i in idList:
            idstr += str(i) + ","
        data = {
            "sort": idstr,
            "jsonp": "jsonp",
            "csrf": "70e8a10f9998293cdb639fa52bacf3ab",
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(7, check['message'])


    '''
    todo:
    收藏夹排序
    对收藏的视频进行各种操作
    '''


if __name__ == '__main__':
    a = BiliFavlist() # 277470241
    a.verifyCookie()
    # a.addFolder('lxymyxdd', 'this is a test message')
    # L = a.getFavlist()
    # a.printFavlist(L)
    # L = L[1 : 10]
    # for i in L:
    #     a.delFolder(i['id'])
    # print(a.getFolderInfo(1328013241))
    # a.changeFolder(1607747941, intro="sbwmyxdd", cover=r"https://wx2.sinaimg.cn/mw2000/005CgOGzly1h1yvun4oklj32jo1bmkjl.jpg")
    # a.moveFolder2(1328013241, 2)