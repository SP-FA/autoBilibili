from enum import Enum


class ExceptionEnum(Enum):
    COOKIE_CONFIG_ERR = 0
    INVALID_COOKIE_ERR = 1

    INVALID_PARAM_ERR = 0
    CREATE_FOLDER_ERR = 1
    DELETE_FOLDER_ERR = 2
    GET_FAVLIST_ERR = 3
    FOLDER_NOT_FOUND_ERR = 4
    GET_FOLDER_INFO_ERR = 5
    CHANGE_FOLDER_INFO_ERR = 6
    MOVE_FOLDER_ERR = 7

    GET_FO_LIST_ERR = 1
    DELETE_FO_GROUP_ERR = 2
    GET_FO_GROUP_ERR = 5
    CREATE_FO_GROUP_ERR = 6
    FO_GROUP_NOT_FOUND_ERR = 7
    CHANGE_FO_GROUP_ERR = 8


class CookieException(Exception):
    """
    ATTRIBUTE:
      @ msg: The error message
      @ errno: The error code
        0: Cookies are not configured in the json file
        1: invalid Cookie
    """
    def __init__(self, err, msg):
        self.errno = err
        self.msg = msg

    def __str__(self):
        return "[Cookie error: %s] %s" % (self.errno.value, self.msg)


class FavlistException(Exception):
    """
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
    """
    def __init__(self, err, msg):
        self.errno = err
        self.msg = msg

    def __str__(self):
        return "[favlist error: %s] %s" % (self.errno.value, self.msg)


class FolistException(Exception):
    """
    ATTRIBUTE:
      @ msg: The error message
      @ errno: The error code
        0: The parameters are invalid
        1: Runtime Failures while getting follow list
        2: Runtime Failures while deleting follow group
        5: Runtime Failures while getting follow group
        6: Runtime Failures while creating follow group
        7: Can not find the follow group
        8: Runtime Failures while changing follow group
    """
    def __init__(self, err, msg):
        self.errno = err
        self.msg = msg

    def __str__(self):
        return "[follow list error: %s] %s" % (self.errno.value, self.msg)
