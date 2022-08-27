from _exception import FolistException
from _util import UtilAcount
from typing import *
from _validation import _checkType


class BiliFolist(UtilAcount):
    def __init__(self, path:str):
        '''
        PARAMETER:
          @ path: the path of the cookies.json file.
        '''
        super().__init__(path)
        self.folist = None


    def getFolist(self, tagid:int=None, pn:int=10, ps:int=50) -> List[Dict]:
        '''
        PARAMETER:
          @ tagid: the id of follow group, None represent for all followed up.
          @ ps: the number of followed ups for each page.
          @ pn: the page number from 1 to pn.

        RETURN:
          a list with each element is a dict contains the info
          of the followed up.
        '''
        _checkType(pn, int)
        _checkType(ps, int)
        _checkType(tagid, int)
        self.folist = []
        for i in range(1, pn+1):
            if tagid == None:
                url = 'https://api.bilibili.com/x/relation/followings?vmid=%s&pn=%d&ps=%d&order=desc&order_type=attention' % (self.uid, i, ps)
            else:
                # checkGroup(tagid)
                url = 'https://api.bilibili.com/x/relation/tag?mid=%s&tagid=%d&pn=%d&ps=%d' % (self.uid, tagid, i, ps)

            check = self.session.get(url, headers=self.headers).json()
            if check['code'] != 0:
                raise FolistException(1, check['message'])
            if tagid == None:
                self.folist += check['data']['list']
            else:
                self.folist += check['data']
        return self.folist


    def printFolist(self, folist:List[Dict]=None):
        '''
        print the list of followed ups. If the parameter folist is None,
        this method will use self.folist. if self.folist is None, it will
        call self.getFolist()

        PARAMETER:
          @ folist: the list contains the info of followed ups.
        '''
        if folist != None:
            printLst = folist
        elif self.folist != None:
            printLst = self.folist
        else:
            printLst = self.getFolist()

        print("total number: %d" % len(printLst))
        print("No.\t       uid\tName")
        for k, i in enumerate(printLst):
            print('%s\t%10s\t%s' % (k, i['mid'], i['uname']))


class BiliFoGroup(UtilAcount):
    def __init__(self, path:str):
        '''
        PARAMETER:
          @ path: the path of the cookies.json file.
        '''
        super().__init__(path)
        self.glst = None


    def getGroups(self) -> List[Dict]:
        '''
        Get all follow groups.

        RETURN:
          a list of json data, which include the info of the follow groups
        '''
        url = "https://api.bilibili.com/x/relation/tags" # ?jsonp=jsonp&callback=__jp3
        check = self.session.get(url, headers=self.headers).json()
        if check['code'] != 0:
            raise FolistException(5, check['message'])
        self.glst = check['data']
        return self.glst


    def printGroup(self, glst:List[Dict]=None):
        '''
        print the groups of followed ups. If the parameter glst is None,
        this method will use self.glst. if self.glst is not None, it will
        call self.getGroups()

        PARAMETER:
          @ folist: the list contains the info of followed ups.
        '''
        if glst != None:
            printLst = glst
        elif self.glst != None:
            printLst = self.glst
        else:
            printLst = self.getGroups()

        print("tagid\t\tname\t\tcount")
        for i in printLst:
            print("%d\t%12s\t\t%5s" % (i['tagid'], i['name'], i['count']))


    def createGroup(self, name:str):
        url = "https://api.bilibili.com/x/relation/tag/create"
        data = {
            "tag": name,
            "jsonp": "jsonp",
            "csrf": "e2aef52ac3ba10aeb2efb4e37336b31c"
        }
        check = self.session.post(url, headers = self.headers, data=data).json()
        if(check['code'] != 0):
            raise FolistException(6, check['message'])


    def checkGroup(self, tagid: int):
        _checkType(tagid, int)
        groupList = self.getGroups()
        for i in groupList:
            if i['tagid'] == tagid:
                return
        raise FolistException(7, "Can not find the follow group")


    def delGroup(self, tagid:int):
        """
        PARAMETER:
          @ tagid: An id of follow group, which you want to delete.
        """
        _checkType(tagid, int)
        self.checkGroup(tagid)
        url = "https://api.bilibili.com/x/relation/tag/del"
        data = {
            "tagid": tagid,
            "jsonp": "jsonp",
            "csrf": "e2aef52ac3ba10aeb2efb4e37336b31c"
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FolistException(2, check['message'])


    def changeGroup(self, tagid:int, name:str):
        _checkType(tagid, int)
        self.checkGroup(tagid)
        url = "https://api.bilibili.com/x/relation/tag/update"
        data = {
            "tagid": tagid,
            "name": name,
            "jsonp": "jsonp",
            "csrf": "e2aef52ac3ba10aeb2efb4e37336b31c"
        }
        check = self.session.post(url, headers=self.headers, data=data).json()
        if check['code'] != 0:
            raise FolistException(8, check['message'])


if __name__ == "__main__":
    b = BiliFolist('../cookies.json')
    b.verifyCookie()
    # folist = b.getFolist(pn=4)
    # b.printFolist()
    c = BiliFoGroup('../cookies.json')
    #c.getGroups()
    c.printGroup()