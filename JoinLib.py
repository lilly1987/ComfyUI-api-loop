import os, sys, glob, json, random, time, copy, string, re
from ConsoleColor import print, console

def textJoin(text,shuffle=False,s=","):
    #print("type : ",type(text))
    if type(text) is dict :
        text=list(text.values())
    #print("type : ",type(text))
    if type(text) is list :
        if shuffle:
            random.shuffle(text)
        text=s.join(text)
    #print("type : ",type(text))
    if type(text) is str  :
        return text

