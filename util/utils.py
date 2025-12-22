
"""
from constants import *
from models.item import Item
from models.room import Room
"""

import random
import textwrap

#region Define help funcs and essential funcs

def return_val_in_list(ar_to_search,val_to_find):
    for i in ar_to_search:
        if i == val_to_find:
            return True

    return False

#Expects and returns a list if list_boolean == true
def wrap_str(string_to_wrap,max_len,list_boolean):

    if not list_boolean:
        wrapped_str = textwrap.fill(string_to_wrap, max_len)

    else:
        wrapped_str = []
        for i in string_to_wrap:
            wrapped_str.append(textwrap.fill(i, max_len))
    return wrapped_str

#endregion
