#!/usr/bin/env python

def riba(s):
    """docstring for riba"""
    return s


def lwrap(list_, w=None):
    """docstring for lwrap"""
    result = []
    o = w or '"'
    for elem in list_:
        result.append(o + elem + o)
    return result
