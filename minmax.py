import os, sys, glob, json, random, time, copy, string, collections

def minmaxf(dic,key,v=None,r=2):
    if key in dic:
        v=dic[key]
    elif f"{key}_min" in dic and f"{key}_max" in dic:
        #print(f"{type}.{key} : true2")
        v=round(random.uniform(dic[f"{key}_min"],dic[f"{key}_max"]),r)
    return v
    
def minmax(dic,key,v=None):
    if key in dic:
        v=dic[key]
    elif f"{key}_min" in dic and f"{key}_max" in dic:
        #print(f"{type}.{key} : true2")
        v=random.randint(dic[f"{key}_min"],dic[f"{key}_max"])
    return v