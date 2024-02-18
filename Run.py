import os, sys, glob, random, time, copy, string, re
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from JoinLib import *
from fileRead import *
from updateLib import *
from queue_prompt import *
from GetLib import *

required  = {'json5','torch'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import json5 as json
import torch



def promptSetInt(prompt,setup,type,key,v=None):
    if key in setup[type]:
        #print(f"{type}.{key} : true1")
        prompt[type]["inputs"][key]= setup[type][key]
    elif f"{key}_min" in setup[type] and f"{key}_max" in setup[type]:
        #print(f"{type}.{key} : true2")
        prompt[type]["inputs"][key]= random.randint(setup[type][f"{key}_min"],setup[type][f"{key}_max"])
    elif v:
        prompt[type]["inputs"][key]= v
        

def promptSetUniform(prompt,setup,type,key):
    
    if key in setup[type]:
        #print(f"{type}.{key} : true1")
        prompt[type]["inputs"][key]= setup[type][key]
    elif f"{key}_min" in setup[type] and f"{key}_max" in setup[type]:
        #print(f"{type}.{key} : true2")
        prompt[type]["inputs"][key]= round(random.uniform(setup[type][f"{key}_min"],setup[type][f"{key}_max"]),2)

def promptSetList(prompt,setup,type,key):
    if key in setup[type]:
        #print(f"{type}.{key} : true")
        prompt[type]["inputs"][key]= randList(setup[type][key])


try:

    ckptCnt=0

    while True:
        
        setup=dicFileRead("setup.json")
        ccolor=setup["ccolor"]
        #print("setup : ",setup)
        
        # -------------------------------------------------
        cuda=torch.cuda.is_available()
        print(f"[{ccolor}]cuda : [/{ccolor}]",cuda)
        if cuda and "cuda" in setup:
            update(setup,setup["cuda"])
        elif not cuda and "cpu" in setup:
            update(setup,setup["cpu"])
        
        # -------------------------------------------------
        if ckptCnt<=0:
            ckptCnt=setup.get("ckptCnt",8)
            ckptList=getFileList(setup["ckptPath"])
            ckpt_path=random.choice(ckptList)
            ckpt_path=pathRemove(ckpt_path,setup["ckptPathSplit"])
            #print("ckpt_path : ",ckpt_path)
            ckpt_name=os.path.splitext(os.path.split(ckpt_path)[1])[0]
            
            vaeList=getFileList(setup["vaePath"])
            vae_path=random.choice(vaeList)
            vae_path=pathRemove(vae_path,setup["vaePathSplit"])
            #print("vae_path  : ",vae_path)
            
        
        
        prompt=jsonFileRead(setup.get("workflow","workflow_api.json"))
        
        # -------------------------------------------------
        prompt["CheckpointLoaderSimple"]["inputs"]["ckpt_name"]= ckpt_path
        
        prompt["VAELoader"]["inputs"]["vae_name"]= vae_path        
        
        # -------------------------------------------------
        prompt["ImpactWildcardEncode1"]["inputs"]["wildcard_text"]= textJoin(
                setup["positive"],
                shuffle=setup.get("shufflepositive",setup.get("shuffle",False))
            )
      
        prompt["ImpactWildcardEncode2"]["inputs"]["wildcard_text"]= textJoin(
                setup["negative"],
                shuffle=setup.get("shufflenegative",setup.get("shuffle",False))
            )
        
        # -------------------------------------------------
        if setup.get("scheduler"):
            #print(f"scheduler : true")
            scheduler=randList(setup["scheduler"])
            prompt["KSampler"]["inputs"]["scheduler"]= scheduler
            prompt["DetailerForEachDebug"]["inputs"]["scheduler"]= scheduler
            
        if setup.get("sampler_name"):
            #print(f"sampler_name : true")
            sampler_name=randList(setup["sampler_name"])
            prompt["KSampler"]["inputs"]["sampler_name"]= sampler_name
            prompt["DetailerForEachDebug"]["inputs"]["sampler_name"]= sampler_name
        # -------------------------------------------------
        type="KSampler"
        if setup.get(type):
            #print(f"{type} : true")
            promptSetInt(prompt,setup,type,"seed",setup.get("seed",random.randint(0, 0xffffffffffffffff )))
            promptSetInt(prompt,setup,type,"steps")
            promptSetUniform(prompt,setup,type,"cfg")
            promptSetList(prompt,setup,type,"sampler_name")
            promptSetList(prompt,setup,type,"karras")
        else:
            prompt[type]["inputs"]["seed"]= setup.get("seed",random.randint(0, 0xffffffffffffffff ))
        
        # -------------------------------------------------
        type="DetailerForEachDebug"
        if setup.get(type):
            #print(f"{type} : true")
            promptSetInt(prompt,setup,type,"seed",setup.get("seed",random.randint(0, 0xffffffffffffffff )))
            promptSetInt(prompt,setup,type,"steps")
            promptSetUniform(prompt,setup,type,"cfg")
            promptSetUniform(prompt,setup,type,"denoise")
            promptSetList(prompt,setup,type,"sampler_name")
            promptSetList(prompt,setup,type,"karras")
        else:
            prompt[type]["inputs"]["seed"]= setup.get("seed",random.randint(0, 0xffffffffffffffff ))
        
        # -------------------------------------------------
        type="ImpactWildcardEncode1"
        if setup.get(type):
            #print(f"{type} : true")
            promptSetInt(prompt,setup,type,"seed",setup.get("seed",random.randint(0, 0xffffffffffffffff )))
        else:
            prompt[type]["inputs"]["seed"]= setup.get("seed",random.randint(0, 0xffffffffffffffff ))
        
        # -------------------------------------------------
        type="ImpactWildcardEncode2"
        if setup.get(type):
            #print(f"{type} : true")
            promptSetInt(prompt,setup,type,"seed",setup.get("seed",random.randint(0, 0xffffffffffffffff )))
        else:
            prompt[type]["inputs"]["seed"]= setup.get("seed",random.randint(0, 0xffffffffffffffff ))
        
        # -------------------------------------------------
        Save_name=f"{ckpt_name}-{time.strftime('%Y%m%d-%H%M%S')}"
        
        if setup.get("SaveImage1",True):
            prompt["SaveImage1"]["inputs"]["filename_prefix"]= Save_name
        else:
            del prompt["SaveImage1"]
            
        if setup.get("SaveImage2",True):
            prompt["SaveImage2"]["inputs"]["filename_prefix"]= Save_name
        else:
            del prompt["SaveImage2"]
        
        # -------------------------------------------------
        print("prompt : ",prompt)
        url=setup["url"]
        queue_prompt(prompt,url=url)
        # -------------------------------------------------
        print(f"[{ccolor}]ckpt_name : [/{ccolor}]{ckpt_name} ; [{ccolor}]ckptCnt : [/{ccolor}]{ckptCnt} ;")
        ckptCnt-=1
        
except Exception:
    console.print_exception()
    quit()