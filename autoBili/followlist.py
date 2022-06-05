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


    def getFolist(self, tagid:int=None, pn:int=10, ps:int=50) -> List[Dict]:
        '''
        Get the follow list.

        PARAMETER:
          @ tagid: the id of follow group, None represent for all followed up.
          @ ps: the number of followed ups for each page.
          @ pn: the page number from 1 to pn.

        RETURN:
          a list with each element is a dict contains the info
          of the followed up.

        EXCEPTION:
          FolistException:
            @ errno 1: Runtime Failures while getting follow list
        '''
        total = 0
        folist = []
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
                folist += check['data']['list']
            else:
                folist += check['data']
        return folist


    def printFolist(self, folist:List[Dict]):
        '''
        print the list of followed ups.

        PARAMETER:
          @ folist: the list contains the info of followed ups.
        '''
        print("total number: %d" % len(folist))
        print("No.\t       uid\tName")
        for k, i in enumerate(folist):
            print('%s\t%10s\t%s' % (k, i['mid'], i['uname']))


# todo:
#   关注分组列表获取 name, id
#   增删改查 关注分组
#   check 关注分组


if __name__ == "__main__":
    b = BiliFolist('../cookies.json')
    b.verifyCookie()
    folist = b.getFolist(pn=4)
    b.printFolist(folist)