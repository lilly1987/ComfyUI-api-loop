import os, sys, glob, json, random, time, copy, string, re
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from fileRead import *
from rich.progress import Progress
from urllib import request
from updateLib import *
import time

required  = {'json5','torch'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
#import json5 as json
import json
import torch


def queue_prompt(prompt,url="http://127.0.0.1:8288/prompt", max=1):
    try:
        with Progress() as progress:
            
            while True:
                if progress.finished:
                    task = progress.add_task("waiting", total=60)
                    
                req =  request.Request(url)        
                response=request.urlopen(req) 
                html = response.read().decode("utf-8")
                ld=json.loads(html)
                
                cnt=ld['exec_info']['queue_remaining']
                
                if cnt <max:
                    progress.stop()
                    break
                progress.update(task, advance=1)
                time.sleep(1)
                
            p = {"prompt": prompt}
            data = json.dumps(p).encode('utf-8')
            req =  request.Request(url, data=data)

        request.urlopen(req)
        print(f"send" )
    except Exception as e:     
        console.print_exception()

    time.sleep(2)
    

try:

    ckptCnt=0

    while True:
        setup=dicFileRead("setup.json")
        ccolor=setup["ccolor"]
        #print("setup : ",setup)
        
        cuda=torch.cuda.is_available()
        print(f"[{ccolor}]cuda : [/{ccolor}]",cuda)
        if cuda and "cuda" in setup:
            update(setup,setup["cuda"])
        elif not cuda and "cpu" in setup:
            update(setup,setup["cpu"])
        
        
        
        if ckptCnt<=0:
            ckptCnt=setup["ckptCnt"]
            ckptList=getFileList(setup["ckptPath"])
            ckpt_path=random.choice(ckptList)
            ckpt_path=pathRemove(ckpt_path,setup["ckptPathSplit"])
            #print("ckpt_path : ",os.path.normpath(ckpt_path))
            #print("ckpt_path : ",os.path.normpath(setup["ckptPathSplit"]))
            #print("ckpt_path : ",ckpt_path)
            #ckpt_path= ckpt_path.replace(setup["ckptPathSplit"],'')
            print("ckpt_path : ",ckpt_path)
            ckpt_name=os.path.splitext(os.path.split(ckpt_path)[1])[0]
            
            vaeList=getFileList(setup["vaePath"])
            vae_path=random.choice(vaeList)
            vae_path=pathRemove(vae_path,setup["vaePathSplit"])
            #print("vae_path  : ",os.path.normpath(vae_path))
            #print("vae_path  : ",os.path.normpath(setup["vaePathSplit"]))
            #print("vae_path  : ",vae_path)
            #vae_path= vae_path.replace(setup["vaePathSplit"],'')
            print("vae_path  : ",vae_path)
            
        print(f"[{ccolor}]ckpt_name : [/{ccolor}]{ckpt_name} ; [{ccolor}]ckptCnt : [/{ccolor}]{ckptCnt} ;")
        
        
        prompt=jsonFileRead("workflow_api.json")
        
        prompt["CheckpointLoaderSimple"]["inputs"]["ckpt_name"]= ckpt_path
        
        prompt["VAELoader"]["inputs"]["vae_name"]= vae_path
        
        prompt["ImpactWildcardEncode1"]["inputs"]["wildcard_text"]= setup["positive"]
      
        prompt["ImpactWildcardEncode2"]["inputs"]["wildcard_text"]= setup["negative"]
        
        
        Save_name=f"{ckpt_name}-{time.strftime('%Y%m%d-%H%M%S')}"
        prompt["SaveImage1"]["inputs"]["filename_prefix"]= Save_name
        prompt["SaveImage2"]["inputs"]["filename_prefix"]= Save_name
        
        prompt["KSampler"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
        prompt["ImpactWildcardEncode1"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
        prompt["ImpactWildcardEncode2"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
        prompt["DetailerForEachDebug"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
        
        #print("prompt : ",prompt)
        url=setup["url"]
        queue_prompt(prompt,url=url)
        ckptCnt-=1
        
except Exception:
    console.print_exception()
    quit()