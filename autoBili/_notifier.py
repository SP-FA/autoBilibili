from win10toast import ToastNotifier


class BiliNotifier(ToastNotifier):
    def showIt(self, info):
        '''
        PARAMETER:
            info = {
                "title": str,
                "msg": str,
                "icon": str,
                "duration": int, float,
            }
        '''
        title = info['title']
        msg = info['msg']
        icon = info['icon']
        duration = info['duration']
        self.show_toast(title, msg, icon, duration)


if __name__ == "__main__":
    toaster = BiliNotifier()

    info = {
        "title": "Example",
        "msg": "This notification is in it's own thread!",
        "icon": "../img/test_icon.ico",
        "duration": 3
    }
    toaster.showIt(info)
