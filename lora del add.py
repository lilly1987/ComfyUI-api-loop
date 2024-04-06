import os, sys, glob, random, time, copy, string, re, numbers
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from pathlib import Path,PurePosixPath
import filecmp
import shutil
# from JoinLib import *
# from fileRead import *
# from updateLib import *
# from queue_prompt import *
# from GetLib import *
# from minmax import *
#sys.path.append("../ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact")
#import wildcards

# required  = {'json5','torch'}
# installed = {pkg.key for pkg in pkg_resources.working_set}
# missing   = required - installed
# if missing:
#     python = sys.executable
#     subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
# import json5 as json
# import torch


def dircmp(p1,p2):
    #p1="../ComfyUI/models/loras"
    #p2="R:/loras"
    fs=filecmp.dircmp(p1, p2)

    fsl=fs.left_only
    for f in fsl:
        p=Path(p1,f)
        print(f"remove : ",p)
        os.remove(p)
    
    fsl=fs.right_only
    for f in fsl:
        p=Path(p2,f)
        if os.path.islink(p):
            print(f"remove",p)
            os.remove(p)
        else:
            print(f"add : ",p1)
            shutil.copy(p, p1)
            
print(sys.argv)

if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit()
    
try:
    print("[green]run[/green]")
    dircmp(sys.argv[1],sys.argv[2])
    #dircmp("../ComfyUI/models/checkpoints/2d","U:/models/checkpoints/2d")
    #dircmp("../ComfyUI/models/loras","U:/models/loras")
    
            
except Exception:
    console.print_exception()
    quit()