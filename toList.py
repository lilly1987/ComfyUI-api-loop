import os, sys, glob, random, time, copy, string, re, numbers, ast
sys.path.append(os.getcwd())
from ConsoleColor import print, console
import mpu.io

#required  = {'json5'}
#installed = {pkg.key for pkg in pkg_resources.working_set}
#missing   = required - installed
#if missing:
#    python = sys.executable
#    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import json5 as json


cOn=True
i1=input("char : ")
if len(i1)==0:    
    with open("toList-c.json", 'r', encoding='utf-8') as file:
        text=file.read()
        l1=ast.literal_eval(text)
    i2=input("x : ")
    if len(i2)>0:
        cOn=False
else:
    l1=[i1]
    
if cOn:
    with open("toList-x.json", 'r', encoding='utf-8') as file:
        text=file.read()
        l2=ast.literal_eval(text)
else:
    l2=[i2]
    
print("l1 :", l1)
print("l2 :", l2)

fm={
    "loras":{
    },
    "lorasUpdate":False,
}

for x in l1 :
    
    for y in l2 :
        fm["loras"]["1"]=x
        fm["loras"]["2"]=y
        print(x,y)
        print(fm)
        fn=f"tmp/{x}-{y}.json"
        mpu.io.write(fn, fm)
        #with open(fn, 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(fm,indent="\t"))
    
    if cOn:
        del fm["lorasUpdate"]
        del fm["loras"]["2"]
        fm["loras"]["1"]=x
        fn=f"tmp/{x}.json"
        mpu.io.write(fn, fm)
        fm["lorasUpdate"]=False