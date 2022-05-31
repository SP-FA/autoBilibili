def _checkIsIn(obj, ctype:str, name:str, contain:list=None):
    '''Checks whether the object is one of several values'''
    _checkType(obj, ctype)
    if ctype in [int, float, bool, str]:
        if obj not in contain:
            raise ValueError("%s need to be one of the following values: %s"
                              % (name, contain))

    ...


def _checkType(obj, ctype):
    '''Check whether the object matches the corresponding type'''
    if obj == None:
        return
    if not isinstance(obj, ctype):
        raise TypeError("%s is needed, not %s" % (ctype, type(obj)))


if __name__ == '__main__':
    x = 5.0
    _checkIsIn(x, float, 'x', contain=[1, 2, 3])