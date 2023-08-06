from ._text import *
import copy, re
from ._collection import NoAssignedValueError
from ._collection import _cli

def action(arguments: list):
    if len(arguments) <2:
        print('''Usage: <name of your original file> <name of your destination file
        without extension> <the file extension of the file you are converting to>
        [next element token, use comma to split] [next line
        token, use comma to split]''')
        raise NoAssignedValueError ( 'No value was passed.')
    argv = copy.copy(arguments)
    argv.split(' ')
    make_decision(argv, len(argv))


def which_type(obj, string: str):
    dotRe = re.compile(r'\.')
    dotRe.sub('', string)
    string = string.lower()
    return {'xlsx':            obj.convert_to_xlsx,
            'csv':             obj.convert_to_csv,
            'dat':             obj.convert_to_binary_file,
            'json':            obj.convert_to_json,
            'keywordnotfound': _cli(string)
            }.get(string, 'keywordnotfound')


def make_decision(option, howmany):
    if howmany == 5:
        with text_file(option[0], option[1], next_ele_token=option[3], next_line_token=option[4]) as f:
            which_type(f, option[2])()
    elif howmany == 4:
        with text_file(option[0], option[1], next_ele_token=option[3]) as f:
            which_type(f, option[2])()
    elif howmany == 3:
        with text_file(option[0], option[1]) as f:
            which_type(f, option[2])()
