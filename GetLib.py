import os, sys, glob, json, random, time, copy, string, collections

def randList(l,v=None):
    t=v
    if type(l) is list:
        t=random.choice(l)
    elif type(l) is str:
        t=l
    return t
