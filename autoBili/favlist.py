from typing import *
from _util import UtilAccount
from _exception import FavlistException, ExceptionEnum
from _validation import _checkType, _checkNumIsBetween, _checkObjIsIn


class BiliFavlist(UtilAccount):
    def __init__(self, cookiePath: str):
        super().__init__(cookiePath)
        self.favList = None

    def get_favlist(self) -> List[Dict]:
        """
        Get the favorite folder list.

        RETURN:
          A list of json data, which include the info of the favorite list
        """
        url = r'https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=' + self.uid
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FavlistException(ExceptionEnum.GET_FAVLIST_ERR, check['message'])
        self.favList = check['data']['list']
        return self.favList

    def print_favlist(self, favList: List[Dict] = None):
        """
        Print the list of favorite folders.

        PARAMETER:
          @ favList: folder list, and the element is the dict of the info of each folder. If it is None
                     this method will use self.favList. And if self.favList is None, it will call self.get_favlist()
        """
        if favList is not None:
            printLst = favList
        elif self.favList is not None:
            printLst = self.favList
        else:
            printLst = self.get_favlist()

        print("\tNo.\t\tfid\t\ttitle")
        for k, i in enumerate(printLst):
            print('%s\t%10s\t%8s\t%s' % (k, i['id'], i['fid'], i['title']))

    def _check_folder(self, mediaId: int):
        """
        Check whether the folder is existed

        PARAMETER:
          @ mediaId: the folder id
        """
        _checkType(mediaId, int)
        mediaList = self.get_favlist()
        for i in mediaList:
            if i['id'] == mediaId:
                return
        raise FavlistException(ExceptionEnum.FOLDER_NOT_FOUND_ERR, "Can not find the folder")

    def add_folder(self, name: str = "", intro: str = "", privacy: int = 0, cover: str = ""):
        """
        Create a new folder

        PARAMETER:
          @ name: folder name
          @ intro: folder introduction
          @ privacy: 0 public, 1 private
          @ cover: cover image link
        """
        _checkType(name, str)
        _checkType(intro, str)
        _checkType(cover, str)
        _checkObjIsIn(privacy, "privacy", [0, 1])
        if name == "":
            raise FavlistException(ExceptionEnum.INVALID_PARAM_ERR, 'A folder name is needed.')
        url = r'https://api.bilibili.com/x/v3/fav/folder/add'
        data = {
            'title': name,
            'intro': intro,
            'privacy': privacy,
            'cover': cover,
            'csrf': self.session.cookies['bili_jct'],
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(ExceptionEnum.CREATE_FOLDER_ERR, check['message'])

    def del_folder(self, mediaId: int):
        """
        Delete a folder

        PARAMETER:
          @ mediaId: The id of the folder
        """
        self._check_folder(mediaId)
        url = r'https://api.bilibili.com/x/v3/fav/folder/del'
        data = {
            "media_ids": mediaId,
            "platform": "web",
            "jsonp": "jsonp",
            "csrf": self.session.cookies['bili_jct'],
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(ExceptionEnum.DELETE_FOLDER_ERR, check['message'])

    def change_folder(self, mediaId: int, title: str = None, intro: str = None, privacy: int = 0, cover: str = None):
        """
        change the information of the folder.

        PARAMETER:
          @ mediaId: the id of the folder.
          @ title: the new folder title.
          @ intro: the new intro of the folder.
          @ cover: the new cover.
        """
        _checkType(title, str)
        _checkType(intro, str)
        _checkType(cover, str)
        _checkObjIsIn(privacy, "privacy", [0, 1])
        raw_data = self.get_folder_info(mediaId)
        url = r'https://api.bilibili.com/x/v3/fav/folder/edit'
        data = {"privacy": 0, "csrf": self.session.cookies['bili_jct'], "media_id": mediaId,
                'title': raw_data['title'] if title is None else title,
                'intro': raw_data['intro'] if intro is None else intro,
                'cover': raw_data['cover'] if cover is None else cover}
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FavlistException(ExceptionEnum.CHANGE_FOLDER_INFO_ERR, check['message'])

    def get_folder_info(self, mediaId: int) -> Dict:
        """
        get folder info

        PARAMETER:
          @ mediaId: the id of the folder

        RETURN:
          a json contains the info
        """
        _checkType(mediaId, int)
        self._check_folder(mediaId)
        url = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&pn=1&ps=20&keyword=&order=mtime&type=0&tid' \
              '=0&platform=web&jsonp=jsonp' % mediaId
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FavlistException(ExceptionEnum.GET_FOLDER_INFO_ERR, check['message'])
        keys = ['id', 'fid', 'title', 'cover', 'cnt_info', 'intro', 'media_count']
        check = check['data']['info']
        info = {}
        for i in keys:
            info[i] = check[i]
        return info

    def move_folder(self, mediaId: int, index: int):
        """
        Move a folder to index, index = 0 is the default favorites folder,
        so index must at least 1 in this method.

        PARAMETER:
          @ mediaId: the folder id you want to move.
          @ index: the index you want to move to.
        """
        _checkType(mediaId, int)
        self._check_folder(mediaId)
        favList = self.get_favlist()
        _checkNumIsBetween(index, "index", 1, len(favList) - 1)

        url = r'https://api.bilibili.com/x/v3/fav/folder/sort'
        idList = []
        for i in favList:
            idList.append(i['id'])
        idList.remove(mediaId)
        try:
            idList.insert(index, mediaId)
        except IndexError:
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
            raise FavlistException(ExceptionEnum.MOVE_FOLDER_ERR, check['message'])

    '''
    todo:
    获取cookie
    收藏夹排序
    对收藏的视频进行各种操作
    win 通知
    '''


if __name__ == '__main__':
    a = BiliFavlist("../cookies.json")
    a.verify_cookie()
    # a.add_folder('lxymyxdd', 'this is a test message')
    # L = a.get_favlist()
    a.print_favlist()
    # a.del_folder(2469068041)
    # print(a.get_folder_info(1731433741))
    # a.change_folder(2384314741, intro="sbwmyxdd")
    # a.move_folder(2384314741, 2)
