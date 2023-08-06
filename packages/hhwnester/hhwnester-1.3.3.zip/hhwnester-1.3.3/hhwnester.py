# -*- coding:utf-8 -*-  
import sys

def print_lol(a_list, indent=False, level=0,fh=sys.stdout):
    """Prints each item in a list, recursively descending
    into nested lists (if necessary)."""

    for each_item in a_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1,fh)
        else:
            if indent:
                for l in range(level):
                    print("\t", end='',file=fh)
            print(each_item,file=fh)