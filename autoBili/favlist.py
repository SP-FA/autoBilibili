import json
import re
from typing import *
from _util import UtilAcount
from _exception import FavlistException
from _validation import _checkType, _checkNumIsIn


class BiliFavlist(UtilAcount):
    def __init__(self, path:str):
        '''
        PARAMETER:
          @ path: the path of the cookies.json file.
        '''
        super().__init__(path)
        self.favList = None


    def getFavlist(self) -> List[Dict]:
        ''' 
        Get the favorite folder list.

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
        self.favList = check['data']['list']
        return self.favList


    def printFavlist(self, favList:List[Dict]):
        '''
        Print the list of favorite folders. If the parameter favList is None,
        this method will use self.favList. if self.favList is None, it will
        call self.getFavlist()

        PARAMETER:
          @ favList: folder list, and the element is the dict of the info of each folder.
        '''
        if favList != None:
            printLst = favList
        elif self.favList != None:
            printLst = self.favList
        else:
            printLst = self.getFavlist()


        print("\tNo.\t\tfid\t\ttitle")
        for k, i in enumerate(printLst):
            print('%s\t%10s\t%8s\t%s' % (k, i['id'], i['fid'], i['title']))


    def checkFolder(self, mediaId:int):
        '''
        Check whether the folder is exist

        PARAMETER:
          @ mediaId: the folder id

        EXCEPTION:
          FavlistException:
          @ errno 4: Can not find the folder
        '''
        _checkType(mediaId, int)
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
        _checkType(name, str)
        _checkType(intro, str)
        _checkType(cover, str)
        _checkNumIsIn(intro, str, "intro", [0, 1])
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
            'csrf': self.session.cookies['bili_jct'],
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
        _checkType(mediaId, int)
        self.checkFolder(mediaId)
        url = r'https://api.bilibili.com/x/v3/fav/folder/del'
        data = {
            "media_ids": mediaId,
            "platform": "web",
            "jsonp": "jsonp",
            "csrf": self.session.cookies['bili_jct'],
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
        _checkType(mediaId, int)
        _checkType(title, str)
        _checkType(intro, str)
        _checkType(cover, str)
        raw_data = self.getFolderInfo(mediaId)
        url = r'https://api.bilibili.com/x/v3/fav/folder/edit'
        data = {
            "privacy": 0,
            "csrf": self.session.cookies['bili_jct'],
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
        _checkType(mediaId, int)
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
        _checkType(mediaId, int)
        self.checkFolder(mediaId)
        favList = self.getFavlist()
        _checkType(index, int, "index", [1, favList.size()-1])
        if index == 0:
            raise FavlistException(0, "index can not be 0, it must at least 1")

        url = r'https://api.bilibili.com/x/v3/fav/folder/sort'
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
            "csrf": self.session.cookies['bili_jct'],
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(7, check['message'])


    '''
    todo:
    获取cookie
    收藏夹排序
    对收藏的视频进行各种操作
    win 通知
    '''


if __name__ == '__main__':
    a = BiliFavlist("../cookies.json")
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