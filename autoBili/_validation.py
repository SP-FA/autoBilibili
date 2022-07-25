def _checkNumIsIn(obj, name:str, contain:list=None, left: float=0, right: float=0):
    '''
    Checks whether the object is one of several values

    PARAMETER:
      @ obj: The object you want to check
      @ name: The name of obj
      @ contain: A list that the obj should be contained in
      @ left & right: The interval which is the range of obj
    '''
    _checkType(obj, [int, float, bool])
    if contain != None:
        if obj not in contain:
            raise ValueError("%s need to be one of the following values: %s"
                              % (name, contain))
    else:
        _checkType(left, int)
        _checkType(right, int)
        if not (left <= obj and right >= obj):
            raise ValueError("%s should between %s and %s" % (name, left, right))


def _checkType(obj, ctype):
    '''
    Check whether the object matches the corresponding type

    PARAMETER:
      @ ctype: A list or a type. If it is a list, obj should be one of its elements.
               If it is a type, the type of obj should equal to ctype.
    '''
    if obj == None:
        return
    
    if isinstance(ctype, list):
        for i in ctype:
            if isinstance(obj, i):
                return
        raise TypeError("%s is needed, not %s" % (ctype, type(obj)))
    else:
        if not isinstance(obj, ctype):
            raise TypeError("%s is needed, not %s" % (ctype, type(obj)))


if __name__ == '__main__':
    x = 5.0
    _checkNumIsIn(x, float, 'x', contain=[1, 2, 3])