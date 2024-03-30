import os, sys, glob, json, random, time, copy, string, collections
from ConsoleColor import print, console, ccolor

# 무조건 업데이트
def dupdate(d, u):
    #print(f"[{ccolor}]dupdate d: [/{ccolor}]",d)
    #print(f"[{ccolor}]dupdate u: [/{ccolor}]",u)
    #try:
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = dupdate(d.get(k, {}), v)
            else:
                d[k] = v
        return d
   #except Exception:
   #    print(f"[{ccolor}]dupdate d: [/{ccolor}]",d)
   #    print(f"[{ccolor}]dupdate u: [/{ccolor}]",u)
   #    console.print_exception()
   #    quit()