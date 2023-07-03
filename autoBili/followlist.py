from _exception import FolistException, ExceptionEnum
from _util import UtilAccount
from typing import *
from _validation import _checkType


class BiliFolist(UtilAccount):
    def __init__(self, cookiePath: str):
        super().__init__(cookiePath)
        self.folist = None

    def get_folist(self, tagid: int = None, pn: int = 10, ps: int = 50) -> List[Dict]:
        """
        PARAMETER:
          @ tagid: the id of follow group, None represent for all followed up.
          @ pn: the page number from 1 to pn.
          @ ps: the number of followed ups for each page.

        RETURN:
          a list with each element is a dict contains the info
          of the followed up.
        """
        _checkType(pn, int)
        _checkType(ps, int)
        self.folist = []
        for i in range(1, pn + 1):
            if tagid is None:
                url = 'https://api.bilibili.com/x/relation/followings?vmid=%s&pn=%d&ps=%d&order=desc&order_type' \
                      '=attention' % (self.uid, i, ps)
            else:
                url = 'https://api.bilibili.com/x/relation/tag?mid=%s&tagid=%d&pn=%d&ps=%d' % (self.uid, tagid, i, ps)

            check = self.session.get(url, headers=self.headers).json()
            if check['code'] != 0:
                raise FolistException(ExceptionEnum.GET_FO_LIST_ERR, check['message'])
            if tagid is None:
                self.folist += check['data']['list']
            else:
                self.folist += check['data']
        return self.folist

    def print_folist(self, folist: List[Dict] = None):
        """
        print the list of followed ups. If the parameter folist is None,
        this method will use self.folist. if self.folist is None, it will
        call self.getFolist()

        PARAMETER:
          @ folist: the list contains the info of followed ups.
        """
        if folist is not None:
            printLst = folist
        elif self.folist is not None:
            printLst = self.folist
        else:
            printLst = self.get_folist()

        print("total number: %d" % len(printLst))
        print("No.\t       uid\tName")
        for k, i in enumerate(printLst):
            print('%s\t%10s\t%s' % (k, i['mid'], i['uname']))


class BiliFoGroup(UtilAccount):
    def __init__(self, cookiePath: str):
        super().__init__(cookiePath)
        self.glst = None

    def get_groups(self) -> List[Dict]:
        """
        Get all follow groups.

        RETURN:
          a list of json data, which include the info of the follow groups
        """
        url = "https://api.bilibili.com/x/relation/tags"  # ?jsonp=jsonp&callback=__jp3
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FolistException(ExceptionEnum.GET_FO_GROUP_ERR, check['message'])
        self.glst = check['data']
        return self.glst

    def print_group(self, glst: List[Dict] = None):
        """
        print the groups of followed ups. If the parameter glst is None,
        this method will use self.glst. if self.glst is not None, it will
        call self.getGroups()

        PARAMETER:
          @ folist: the list contains the info of followed ups.
        """
        if glst is not None:
            printLst = glst
        elif self.glst is not None:
            printLst = self.glst
        else:
            printLst = self.get_groups()

        print("tagid\t\tname\t\tcount")
        for i in printLst:
            print("%d\t%12s\t\t%5s" % (i['tagid'], i['name'], i['count']))

    def create_group(self, name: str):
        url = "https://api.bilibili.com/x/relation/tag/create"
        data = {
            "tag": name,
            "jsonp": "jsonp",
            "csrf": "e2aef52ac3ba10aeb2efb4e37336b31c"
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FolistException(ExceptionEnum.CREATE_FO_GROUP_ERR, check['message'])

    def _check_group(self, tagid: int):
        _checkType(tagid, int)
        groupList = self.get_groups()
        for i in groupList:
            if i['tagid'] == tagid:
                return
        raise FolistException(ExceptionEnum.FO_GROUP_NOT_FOUND_ERR, "Can not find the follow group")

    def delGroup(self, tagid: int):
        """
        PARAMETER:
          @ tagid: An id of follow group, which you want to delete.
        """
        _checkType(tagid, int)
        self._check_group(tagid)
        url = "https://api.bilibili.com/x/relation/tag/del"
        data = {
            "tagid": tagid,
            "jsonp": "jsonp",
            "csrf": "e2aef52ac3ba10aeb2efb4e37336b31c"
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FolistException(ExceptionEnum.DELETE_FO_GROUP_ERR, check['message'])

    def change_group(self, tagid: int, name: str):
        _checkType(tagid, int)
        self._check_group(tagid)
        url = "https://api.bilibili.com/x/relation/tag/update"
        data = {
            "tagid": tagid,
            "name": name,
            "jsonp": "jsonp",
            "csrf": "e2aef52ac3ba10aeb2efb4e37336b31c"
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FolistException(ExceptionEnum.CHANGE_FO_GROUP_ERR, check['message'])


if __name__ == "__main__":
    # b = BiliFolist('../cookies.json')
    # b.verify_cookie()
    # folist = b.get_folist(pn=4)
    # b.print_folist()
    c = BiliFoGroup('../cookies.json')
    # c.get_groups()
    c.print_group()
