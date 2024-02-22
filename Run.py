import os, sys, glob, random, time, copy, string, re
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from JoinLib import *
from fileRead import *
from updateLib import *
from queue_prompt import *
from GetLib import *
from minmax import *

required  = {'json5','torch'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import json5 as json
import torch







def promptSetInt(prompt,setup,type,key,v=None):
    v2=minmax(setup.get(type,setup),key)
    if v2:
        prompt[type]["inputs"][key]= v2
    elif v:
        prompt[type]["inputs"][key]= v
        
def promptSetUniform(prompt,setup,type,key,v=None):
    v2=minmaxf(setup.get(type,setup),key)
    if v2:
        prompt[type]["inputs"][key]= v2
    elif v:
        prompt[type]["inputs"][key]= v
        
def promptSetList(prompt,setup,type,key,v=None):
    v2=setup.get(type,setup).get(key)
    if v2:
        prompt[type]["inputs"][key]= randList(v2)
    elif v:
        prompt[type]["inputs"][key]= v
    


try:

    ckptCnt=0
    ckptMax=0
    jitemCnt=0
    jitemMax=0

    while True:
        
        setup=dicFileRead("setup.json")
        ccolor=setup["ccolor"]
        #print("setup : ",setup)
        
        # -------------------------------------------------
        cuda=torch.cuda.is_available()
        #print(f"[{ccolor}]cuda : [/{ccolor}]",cuda)
        if cuda and "cuda" in setup:
            update(setup,setup["cuda"])
        elif not cuda and "cpu" in setup:
            update(setup,setup["cpu"])
            
        # -------------------------------------------------
        if jitemCnt<=0:
            
            jlist=getFileList("list/**/*.json")
            #print("jlist1 : ",jlist)
            
            listMatchs=setup.get("listMatch",["*"])
            listMatch=random.choice(listMatchs)
            #print("listMatch : ",listMatch)
            
            jlist=[ i for i in jlist if i.match(f"list/{listMatch}.json")]
            #print("jlist2 : ",jlist)
            if len(jlist)==0:
                print("no listMatchs : ", listMatchs)
                continue
            
            jchoice=random.choice(jlist)
            #print("jchoice : ",jchoice)
            jitem=dicFileRead(jchoice)
            jitem_name=os.path.splitext(os.path.split(jchoice)[1])[0]
            
            #print("jitem_name : ",jitem_name)
            
            jitemMax=jitemCnt=setup.get("itemCnt",8)
            
        update(setup,jitem)
        
        # -------------------------------------------------
        if ckptCnt<=0:
            ckptMax=ckptCnt=setup.get("ckptCnt",8)
            
            if random.random() < setup.get("ckptPer",0) :
                ckptList=dicFileRead("ckpt.json")
            else:
                ckptList=getFileList(setup["ckptPath"])
            
            ckpt_path=random.choice(ckptList)
            ckpt_path=pathRemove(ckpt_path,setup["ckptPathSplit"])
            
            
            #print("ckpt_path : ",ckpt_path)
            ckpt_name=os.path.splitext(os.path.split(ckpt_path)[1])[0]
            
            vaeList=getFileList(setup["vaePath"])
            vae_path=random.choice(vaeList)
            vae_path=pathRemove(vae_path,setup["vaePathSplit"])
            vae_name=os.path.splitext(os.path.split(vae_path)[1])[0]
            #print("vae_path  : ",vae_path)
            
        
        
        prompt=jsonFileRead(setup.get("workflow","workflow_api.json"))
        
        # -------------------------------------------------
        prompt["CheckpointLoaderSimple"]["inputs"]["ckpt_name"]= ckpt_path
        
        prompt["VAELoader"]["inputs"]["vae_name"]= vae_path        

        
        # -------------------------------------------------
        scheduler=None
        if setup.get("scheduler"):
            scheduler=randList(setup["scheduler"])
            
        sampler_name=None
        if setup.get("sampler_name"):
            sampler_name=randList(setup["sampler_name"])            
        
        #steps=None
        #if setup.get("steps"):
        steps=minmax(setup,"steps")
            
        #cfg=None
        #if setup.get("cfg"):
        cfg=minmaxf(setup,"cfg")

        # -------------------------------------------------
        type="CLIPSetLastLayer"

        promptSetInt(prompt,setup,type,"stop_at_clip_layer")
        # -------------------------------------------------
        type="KSampler"

        promptSetInt(prompt,setup,type,"seed",random.randint(0, 0xffffffffffffffff ))
        promptSetInt(prompt,setup,type,"steps",steps)
        promptSetUniform(prompt,setup,type,"cfg",cfg)
        promptSetList(prompt,setup,type,"sampler_name",sampler_name)
        promptSetList(prompt,setup,type,"scheduler",scheduler)

        
        # -------------------------------------------------
        type="DetailerForEachDebug"

        promptSetInt(prompt,setup,type,"seed",random.randint(0, 0xffffffffffffffff ))
        promptSetInt(prompt,setup,type,"steps",steps)
        promptSetUniform(prompt,setup,type,"cfg",cfg)
        promptSetUniform(prompt,setup,type,"denoise")
        promptSetList(prompt,setup,type,"sampler_name",sampler_name)
        promptSetList(prompt,setup,type,"scheduler",scheduler)

        
        # -------------------------------------------------
        type="ImpactWildcardEncode1"
        promptSetInt(prompt,setup,type,"seed",random.randint(0, 0xffffffffffffffff ))

        # -------------------------------------------------
        type="ImpactWildcardEncode2"
        promptSetInt(prompt,setup,type,"seed",random.randint(0, 0xffffffffffffffff ))

        # -------------------------------------------------
        tm=time.strftime('%Y%m%d-%H%M%S')
        # Save_name=f"{ckpt_name}-{time.strftime('%Y%m%d-%H%M%S')}"
        
        if setup.get("SaveImage1",True):
            sampler_name1=prompt["KSampler"]["inputs"]["sampler_name"]
            scheduler1=prompt["KSampler"]["inputs"]["scheduler"]
            prompt["SaveImage1"]["inputs"]["filename_prefix"]= f"{ckpt_name}-{sampler_name1}-{scheduler1}-{jitem_name}-{tm}"
        else:
            del prompt["SaveImage1"]
            
        if setup.get("SaveImage2",True):
            sampler_name1=prompt["DetailerForEachDebug"]["inputs"]["sampler_name"]
            scheduler1=prompt["DetailerForEachDebug"]["inputs"]["scheduler"]
            prompt["SaveImage2"]["inputs"]["filename_prefix"]= f"{ckpt_name}-{sampler_name1}-{scheduler1}-{jitem_name}-{tm}"
        else:
            del prompt["SaveImage2"]
        
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
        
        if setup.get("jitem show"):
            print("jitem : ",jitem)
        if setup.get("prompt show"):
            print("prompt : ",prompt)
        #print( prompt["ImpactWildcardEncode1"]["inputs"]["seed"])
        #print( prompt["ImpactWildcardEncode2"]["inputs"]["seed"])
        #print( prompt["KSampler"]["inputs"]["seed"])
        #print( prompt["DetailerForEachDebug"]["inputs"]["seed"])
        #print( prompt["KSampler"]["inputs"]["steps"])
        #print( prompt["DetailerForEachDebug"]["inputs"]["steps"])
        #print( prompt["KSampler"]["inputs"]["cfg"])
        #print( prompt["DetailerForEachDebug"]["inputs"]["cfg"])
        #print( prompt["KSampler"]["inputs"]["sampler_name"])
        #print( prompt["DetailerForEachDebug"]["inputs"]["sampler_name"])
        #print( prompt["KSampler"]["inputs"]["scheduler"])
        #print( prompt["DetailerForEachDebug"]["inputs"]["scheduler"])
        
        # -------------------------------------------------s
        url=setup["url"]
        queue_cnt=setup.get("queue_cnt",1)
        for i in range(queue_cnt):
            print(f"{ckpt_name} ; {ckptCnt}/{ckptMax} ; {jitemCnt}/{jitemMax} ; {queue_cnt-i}/{queue_cnt} ; {vae_name} ; {cuda} ; {jitem_name} ;")
            if setup.get("queue_prompt"):
                queue_prompt(prompt,url=url)
        # -------------------------------------------------
        ckptCnt-=1
        jitemCnt-=1
        # -------------------------------------------------
except Exception:
    console.print_exception()
    quit()