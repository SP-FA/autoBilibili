import math
import os
import re
import time
import warnings
from typing import *

from tqdm import tqdm
from autoBili._util import UtilAccount
from lxml import etree
import json

from autoBili._validation import _checkType


class SearchVideos(UtilAccount):
    def __init__(self, path):
        super().__init__(path)
        self.videoLst = []
        self.videoPath = []

    def search_and_download(self, content, num, rootPath):
        """
        Search videos and download them

        PARAMETER:
          @ content: Things you want to search.
          @ num: Total search numbers you want to get.
          @ rootPath: The root path you want to save the files.
        """
        self.search_videos(content, num)
        self._create_folder(rootPath)

        pbar = tqdm(range(0, len(self.videoLst)))
        pbar.set_description("[Downloading videos]")
        for i in pbar:
            path = os.path.join(self.videoPath[i], "1.mp3")
            url = self.videoLst[i]["arcurl"]
            self._download_file(path, url)

    def search_videos(self, content, num) -> List[Dict]:
        """
        Search videos

        PARAMETER:
          @ content: Things you want to search.
          @ num: Total search numbers you want to get.
        """
        _checkType(num, int)
        pages = math.ceil(num / 20)
        residue = num % 20
        pbar = tqdm(range(1, pages + 1))
        pbar.set_description("[Searching videos]")
        for i in pbar:
            url = "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=%s&page=%d" % (content, i)
            searchResult = self.session.get(url, headers=self.headers).json()
            result = searchResult['data']
            result = result['result']
            result = [i for i in result if i['result_type'] == "video"]
            result = result[0]['data']
            self.videoLst.extend(result)
            time.sleep(0.1)

        if residue != 0:
            self.videoLst = self.videoLst[:-(20 - residue)]

        return self.videoLst

    def _create_folder(self, rootPath):
        """
        Create folders for each video.

        PARAMETER:
          @ rootPath: The root path you want to save the files.
        """
        match = re.compile(r'(<.*?>)|\||;|\\|/|<|>|:|\?|\*|"')
        pbar = tqdm(self.videoLst)
        pbar.set_description("[Creating folders]")
        for i in pbar:
            name = i["title"]
            name = match.sub(" ", name)
            path = os.path.join(rootPath, name)
            self.videoPath.append(path)
            if not os.path.exists(path):
                os.mkdir(path)

    def _download_file(self, path, url):
        """
        Download the file corresponding to the url.

        PARAMETER:
          @ path: The path including the file name you want to save.
          @ url: The website url of this video.
        """
        try:
            response = self.session.get(url, headers=self.headers)
            _element = etree.HTML(response.content)
            # 获取 window.__playinfo__ 的json对象,[20:]表示截取'window.__playinfo__='后面的json字符串
            videoPlayInfo = str(_element.xpath('//head/script[3]/text()')[0].encode('utf-8').decode('utf-8'))[20:]
            response = json.loads(videoPlayInfo)
        except Exception:
            return

        try:
            # 2018年以后的b站视频由.audio和.video组成
            audioURl = response['data']['dash']['audio'][0]['baseUrl']
            self._download(homeurl=url, url=audioURl, name=path)
        except Exception:
            try:
                # 2018年以前的b站视频音频视频结合在一起,后缀为.flv
                videoURL = response['data']['durl'][0]['url']
                self._download(homeurl=url, url=videoURL, name=path)
            except Exception:
                return

    def _download(self, homeurl, url, name):
        """

        PARAMETER:
          @ homeurl: The website url of this video.
          @ url: The source of the file.
          @ name: Save path including file name.
        """
        headers = self.headers.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # 添加请求头键值对,写上 refered:请求来源
            headers.update({'Referer': homeurl})
            # 发送option请求服务器分配资源
            self.session.options(url=url, headers=headers, verify=False)
            begin = 0
            end = 1024 * 512 - 1
            flag = 0
            loopNumber = 0
            while True:
                loopNumber += 1
                # 添加请求头键值对,写上 range:请求字节范围
                headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
                # 获取视频分片
                res = self.session.get(url=url, headers=headers, verify=False)
                if res.status_code != 416:
                    # 响应码不为为416时有数据
                    begin = end + 1
                    end = end + 1024 * 512
                else:
                    headers.update({'Range': str(end + 1) + '-'})
                    res = self.session.get(url=url, headers=headers, verify=False)
                    flag = 1
                with open(name, 'ab') as fp:
                    fp.write(res.content)
                    fp.flush()
                    if flag == 1 or loopNumber >= 5000:
                        fp.close()
                        break


if __name__ == "__main__":
    sv = SearchVideos("../cookies.json")
    sv.search_and_download("洛天依", 1000, r"H:\projectLuo\audio")
