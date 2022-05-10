# autoBilibili
 辅助自动化管理 bilibili

## class: BiliFolder
用于操作 bilibili 的收藏夹

包含的方法：

- `__init__(self, uid)`:
    
    初始化，需要输入用户 uid，并手动配置 cookie

- `verifyCookie(self)`:
    
    验证 Cookie 是否可用

    异常：

    - CookieException 0: 无效的 Cookie

    - CookieException 1: 初始化方法中未配置 cookie

- `addFolder(self, name:str="", intro:str="", privacy:int=0, cover:str="")`:
    
    创建新收藏夹

    参数：

    - name: 收藏夹名

    - intro: 收藏夹简介

    - privacy: 可见性，0 为公开，1 为私密

    - cover: 封面图片链接

    异常：

    - FavlistException 0: 运行失败
    
    - FavlistException 1: 参数不符合要求