import re

def get_currency(s):
    currencies = ['$','€','£']
    for cur in currencies:
        if cur in s:
            return cur

def remove_spaces_around(s):
    cur = '$'
    cur_index = s.index(cur)
    if cur_index != 0:
        if s[cur_index - 1] == ' ':
            s = s[0:cur_index-1] + s[cur_index:]
    cur_index = s.index(cur)
    if cur_index != len(s) -1:
        if s[cur_index + 1] == ' ':
            s = s[0:cur_index+1] + s[cur_index+2:]
    return s

def get_amount_str(string_amount):
    """Extract amount if pre currency sign"""
    if str(string_amount) != 'nan':
        currency = get_currency(string_amount)
        if currency:
            string_amount = remove_spaces_around(string_amount)
        regex = ["(?:[\£\$\€]{1}[,\d]+.?\d*)","(?:[,\d]+.?\d*)[\£\$\€]","(?:[,\d]+.?\d*)"]
        for reg in regex:
            result = re.findall(reg,string_amount)
            if result:
                return result[0].strip()