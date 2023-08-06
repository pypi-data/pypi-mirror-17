from ._collection import simplify_str
import os as _os
import sys as _sys

true = True
false = False


def search_file(name, *path, **option):
    """Search the given file name(re pattern) in the given path, if path
    is none, will search in C:\\(It will search in the order
    you let it to). If enable list_all, it will return a
    tuple containing all result."""
    from ._collection import compare
    if len(path) == 0:
        path = 'C:\\'
    I, topDown, list_all = false, true, false
    size = _sys.maxsize
    for key, value in option.items():
        if key == 'caseI':
            I = option['caseI']
        elif key == 'topdown':
            topDown = option['topdown']
        elif key == 'list_all':
            list_all = option['list_all']
        elif key == 'size':
            size = option['size']
        else:
            raise KeyError('No such option.')
    temp = []
    for i in path:
        for current_folder, subfolder, subfile in _os.walk(i, topdown=topDown):
            for fname in subfile:
                if compare(fname, name, i=I):
                    if list_all and _os.path.getsize(_os.path.join(current_folder, fname)) / 1024 <= size:
                        temp.append(_os.path.abspath(_os.path.join(current_folder, fname)))
                    elif _os.path.getsize(_os.path.join(current_folder, fname)) / 1024 <= size:
                        return _os.path.abspath(_os.path.join(current_folder, fname))
    if len(temp) > 0:
        return tuple(temp)
    return None


def search_folder(name, *path, **option):
    """Search the given folder name(re pattern) in the given path, if path
    is none, will search in C:\\(It will search in the order
    you let it to). If enable list_all, it will return a
    tuple containing all result."""
    from ._collection import compare
    if len(path) == 0:
        path = 'C:\\'
    I, topDown, list_all, empty = false, true, false, false
    size = _sys.maxsize
    for key, value in option.items():
        if key == 'caseI':
            I = option['caseI']
        elif key == 'topdown':
            topDown = option['topdown']
        elif key == 'list_all':
            list_all = option['list_all']
        elif key == 'size':
            size = option['size']
        elif key == 'ignore_empty_folder':
            empty = option['ignore_empty_folder']
        else:
            raise KeyError('No such option.')
    temp = []
    for i in path:
        for current_folder, subfolder, subfile in _os.walk(i, topdown=topDown):
            for fname in subfolder:
                if compare(fname, name, i=I):
                    if empty == false:
                        if list_all and _os.path.getsize(_os.path.join(current_folder, fname)) / 1024 <= size:
                            temp.append(_os.path.abspath(_os.path.join(current_folder, fname)))
                        elif _os.path.getsize(_os.path.join(current_folder, fname)) / 1024 <= size:
                            return _os.path.abspath(_os.path.join(current_folder, fname))
                    else:
                        if _os.listdir(_os.path.join(current_folder, fname)) == '':
                            continue
                        if list_all and _os.path.getsize(_os.path.join(current_folder, fname)) / 1024 <= size:
                            temp.append(_os.path.abspath(_os.path.join(current_folder, fname)))
                        elif _os.path.getsize(_os.path.join(current_folder, fname)) / 1024 <= size:
                            return _os.path.abspath(_os.path.join(current_folder, fname))
    if len(temp) > 0:
        return tuple(temp)
    return None


def parselist(src: str, caseI=False):
    """Parse a string into list: '[1,2,3]'>-[1,2,3].
    If their is some problem with the string containing
    the list, it would probably give an incorrect result."""
    from ._collection import switch_bool

    src = src[1:-1] + ','
    in_quote, reading = false, false
    part = ''
    final = []

    for i in src:
        if in_quote == false and i == ']':
            part += i
            part = (parselist(part))
            reading = false

        elif (in_quote == false and i == '[') or reading == true:
            reading = true
            part += i
            continue
        elif i == '\'':
            try:
                if i[src.index(i) + 1] == ',' or i[src.index(i) - 1] == ',':
                    in_quote = switch_bool(in_quote)
            except IndexError:
                pass

        elif i == ',' and in_quote == false:
            final.append(part)
            part = ''

        elif in_quote:
            part += i
        else:
            part = simplify_str(i, casei=caseI).simplify()

    return final
