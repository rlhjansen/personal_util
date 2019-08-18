

def index_alt_return(iterable, required_value, altfunc, target='iterable'):
    """ Returns index of required value in list.

    if unable to find the required value this function returns
        value determined by altfunc and its target.

    args:
        iterable: iterable
        required_value: anything you'd likely want the index of
        altfunc: whatever should be the function to return index
        target: String, either 'iterable', 'reqval', 'none' or 'both'
            target argument determines wheter altfunc is applied to the iterable
            ,the required value, none or both, yielding different
            possible applications.

            In case target='both', altfunc should assume:
                altfunc(iterable, required_value)

    Example Usage:
        >>> mystring = 'foobar'
        >>> index_alt_return(mystring, 'crow', len, target='reqval')
        4

        >>> index_alt_return(mystring, 'crow', len, target='iterable')
        6
    """
    alt_argument = eval(target)
    try:
        ind = iterable.index(required_value)
        return ind
    except ValueError:
        if target == 'iterable':
            return altfunc(iterable)
        elif target == 'reqval':
            return altfunc(required_value)
        elif target == 'none':
            return altfunc()
        if target == 'both':
            return altfunc(iterable, required_value)
        return len(iterable)
