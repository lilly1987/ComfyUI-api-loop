import sys
import ast
import re
import glob,os
#from wcmatch import pathlib
from pathlib import Path,PurePosixPath
import shutil, time
import subprocess
import pkg_resources
from ConsoleColor import print, console
from updateLib import *

required  = {'json5'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import json5 
import json

comment = re.compile(r"#.*")

def jsonFileRead(path,text=""):
    try:
        text=""
        #print("jsonFileRead : ",path)
        with open(path, 'r', encoding='utf-8') as file:
            text=file.read()
            #comment.sub("", text)
            #text=ast.literal_eval(text)
            #text=json.dumps(text)
            #text=json.loads(text)
            text=json5.loads(text)
            #text=json.load(file)
            #text=json.loads(file)
            #text=json.dumps(file)
            #print(type(text))
        return text
    except Exception:
        print("text : ",text,style="reset")
        console.print_exception()
        print("path : ",path,style="reset")
        quit()
        
def dicFilesRead(path):
    try:
        #print("dicFilesRead : ",path)
        files=getFileList(path)
        d={}
        u={}
        f=None
        for f in files:
            #print("dicFilesRead : ",f)
            #dupdate(d,dicFileRead(f))
            u=dicFileRead(f)
            d.update(u)
        return d
    except Exception:
        print("d : ",d,style="reset")
        print("u : ",u,style="reset")
        console.print_exception()
        print("path : ",path,style="reset")
        print("f : ",f,style="reset")
        quit()        
        
def dicFileRead(path):
    try:
        #print("dicFileRead : ",path)
        text=""
        with open(path, 'r', encoding='utf-8') as file:
            text=file.read()
            comment.sub("", text)
            text=text.replace('true', 'True')
            text=text.replace('false', 'False')
            text=ast.literal_eval(text)
            #text=json.dumps(text)
            #text=json.loads(text)
        return text
    except Exception:
        print("text : ",text,style="reset")
        console.print_exception()
        print("path : ",path,style="reset")
        quit()
        
def getFileList(path,filelist=[]):
    try:
        filelist=list(Path().rglob(path))
        #print(filelist)
        #print(type(filelist))
        return filelist
    except Exception:
        print("filelist : ",filelist,style="reset")
        console.print_exception()
        print("path : ",path,style="reset")
        quit()
        
def pathRemove(opath,rpath):
    try:
        #opath=os.path.normpath(opath)
        #rpath=os.path.normpath(rpath)
        opath=Path(opath)
        rpath=Path(rpath)
        opath=opath.as_posix()
        rpath=rpath.as_posix()
        opath=opath.replace(rpath+'/','')
        opath=os.path.normpath(opath)
        #print(opath)
        #print(rpath)
        #print(type(filelist))
        return opath
    except Exception:
        print("opath : ",opath,style="reset")
        print("rpath : ",rpath,style="reset")
        console.print_exception()
        quit()
        