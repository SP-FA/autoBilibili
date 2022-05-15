# autoBilibili
使用 python 构建一个辅助自动化管理 bilibili 的 package。



## 自动登陆 Bilibili
首先需要获取账户的 Cookie，填入 `__init__` 方法中，此功能目前还在完善。

可通过如下代码验证 Cookie 是否配置正确
```python
bili = BiliFavlist()
bili.verifyCookie()
```
如果配置完善，则程序会打印 "Valid Cookie, user name: + 用户名"

## 新建收藏夹
**函数声明：**

`addFolder(self, name:str="", intro:str="", privacy:int=0, cover:str="")`
 
参数：
- `name`：收藏夹的名字，不能为空
- `intro`：收藏夹简介
- `privacy`：可见性，0 代表公开，1 代表私密
- `cover`：收藏夹封面，需要是图片链接

e.g.
```python
bili.addFolder("folder name", "folder intro", 0)
```


## 获取收藏夹列表 & 打印
**函数声明：**

`getFavlist(self) -> List[Dict]`

返回值：一个 list，元素是 dict，包含了每个收藏夹的信息。

`printFavlist(self, favList:List[Dict])`

参数：
- `favList`：获取到的收藏夹列表，是一个 list，元素是 dict 包含了每个收藏夹的信息

e.g.

<html>
<style>
    .mac {
        width:10px;
        height:10px;
        border-radius:5px;
        float:left;
        margin:10px 0 0 5px;
    }
    .b1 {
        background:#E0443E;
        margin-left: 10px;
    }
    .b2 { background:#DEA123; }
    .b3 { background:#1AAB29; }
    .warpper{
        background:#121212;
        border-radius:5px;
        width:400px;
    }
</style>
<div class="warpper">
    <div class="mac b1"></div>
    <div class="mac b2"></div>
    <div class="mac b3"></div>
<div>
<br>
</html>

```python
lst = bili.getFavlist()
bili.printFavlist(lst)
```


## 删除收藏夹
**函数声明：**

`delFolder(self, mediaId:int)`

参数：
- `mediaId`：收藏夹 id

e.g.
```python
lst = bili.getFavlist()
lst = lst[1:] // 去掉默认收藏夹
for i in lst:
    bili.delFolder(i['id']) // 删除所有收藏夹
```


## 获取收藏夹信息 & 修改信息
**函数声明：**

`getFolderInfo(self, mediaId:int) -> Dict`

参数：
- `mediaId`：收藏夹 id

返回值：一个字典，包含了该收藏夹的详细信息

`changeFolder(self, mediaId:int, title:str=None, intro:str=None, cover:str=None)`

参数：
- `mediaId`：要修改信息的收藏夹 id
- `title`：修改后的收藏夹名。为空则表示不修改，下同。
- `intro`：修改后的简介
- `cover`：修改后的封面图片链接

e.g.
```python
lst = bili.getFavlist()
i = lst[1]
print(bili.getFolderInfo(i['id']))
bili.changeFolder(i['id'], 'changedTitle', 'Test changing info')
print(bili.getFolderInfo(i['id']))
```


## 移动收藏夹
**函数声明：**

`moveFolder2(self, mediaId:int, index:int)`

参数：
- `mediaId`：要移动的收藏夹 id
- `index`：要移动到的位置。注意，这里的位置要从 1 开始，因为 0 是默认收藏夹，且列表要去掉要移动的收藏夹，也就是说，如果有 n 个收藏夹，那么 index 的取值范围是 [1, n)

e.g.
```python
lst = bili.getFavlist()
i = lst[1]
bili.printFavlist(lst)
bili.moveFolder2(i['id'], 2)
bili.printFavlist(bili.getFavlist())
```

可能会引发的异常：
- CookieException
    - 0：没有配置 Cookie
    - 1：Cookie 不正确
- FavlistException
    - 0：参数错误
    - 1：收藏夹创建失败
    - 2：删除收藏夹失败
    - 3：获取列表失败
    - 4：无法找到收藏夹
    - 5：获取收藏夹信息时出错
    - 6：修改收藏夹信息失败
    - 7：移动收藏夹时出错

---

to do：
1. 收藏夹排序
2. 对收藏的视频进行操作