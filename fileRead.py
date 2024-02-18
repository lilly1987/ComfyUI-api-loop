import sys
import ast
import re
import glob,os
import shutil, time
import subprocess
import pkg_resources
from pathlib import Path
from ConsoleColor import print, console

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
        
def dicFileRead(path,text=""):
    try:
        text=""
        #print("dicFileRead : ",path)
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
        filelist=glob.glob(path,recursive=True)
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
        