def _checkObjIsIn(obj, name: str, contain: list):
    """
    This function will check whether the object is one of several values in a given list'

    PARAMETER:
      @ obj: The object you want to check
      @ name: The name of obj
      @ contain: A list that the obj should be contained in
    """
    if obj not in contain:
        raise ValueError("%s need to be one of the following values: %s" % (name, contain))


def _checkNumIsBetween(obj, name: str, left: float = 0, right: float = 0):
    """
    This function will check whether the number is between [left, right]

    PARAMETER:
      @ obj: The object you want to check
      @ name: The name of obj
      @ left & right: The interval which is the range of obj
    """
    _checkType(obj, [int, float])
    _checkType(left, [int, float])
    _checkType(right, [int, float])
    if not (left <= obj <= right):
        raise ValueError("%s should between %s and %s" % (name, left, right))


def _checkType(obj, ctype):
    """
    Check whether the object matches the corresponding type.

    PARAMETER:
      @ obj: The object you want to check
      @ ctype: A list or a type. If it is a list, obj should be one of its elements.
               If it is a type, the type of obj should equal to ctype.
    """
    if obj is None:
        return

    if isinstance(ctype, list):
        for i in ctype:
            if isinstance(obj, i):
                return
    else:
        if isinstance(obj, ctype):
            return
    raise TypeError("%s is needed, not %s" % (ctype, type(obj)))


if __name__ == '__main__':
    x = 5.0
    _checkObjIsIn(x, 'x', contain=[1, 2, 3])
