import os, sys, glob, json, random, time, copy, string, re
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from fileRead import *
from rich.progress import Progress
from urllib import request
import time

required  = {'json5'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
#import json5 as json
import json



url="http://127.0.0.1:8288/prompt"

def queue_prompt(prompt, max=1):
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

    setup=jsonFileRead("setup.json")
    
    prompt=jsonFileRead("workflow_api.json")
    
    ckpt_path= "2d\\xFlareMixS2_anime.safetensors"
    prompt["CheckpointLoaderSimple"]["inputs"]["ckpt_name"]= ckpt_path
    prompt["VAELoader"]["inputs"]["vae_name"]= "Anything-V3.0.vae.pt"
    
    prompt["ImpactWildcardEncode1"]["inputs"]["wildcard_text"]= "masterpiece , best quality , detailed_face, cowboy shot, {from side,|9::} looking at viewer,1girl,  __char__,__chest__ , __exposure__,  thin waist,sex, large insertion, dildo riding , dildo, object insertion,{arms behind back, bound arms, bound bdsm, bdsm, |}{(open_dress:1.0), (Undressing:1.1), Nipples, (Pussy:1.1), (navel:1.0),|2::}__shoulder__,{See Through,|}__concept__,__insertion__, {<lora:microwaistV05:{0.75|0.875|1.0}:1.0>,|3::} , "
    prompt["ImpactWildcardEncode2"]["inputs"]["wildcard_text"]= "lowres, worst quality, low quality,cropped, (multiple views), (multiple viewer), (cropped), face only, facial, lower body, from torso down,{-$$embedding:FastNegativeV2.pt|embedding:NGH.safetensors|embedding:bad_prompt_version2-neg.pt|embedding:negative_hand-neg|embedding:nncursedV0-neg.pt|embedding:badquality.pt|embedding:bad-picture-chill-75v.pt|embedding:neg_grapefruit.pt|embedding:ParaNegative.safetensors|embedding:easynegative.safetensors|embedding:EasyNegativeV2.safetensors},(monochrome:1.1), "
    
    ckpt_name=os.path.splitext(os.path.split(ckpt_path)[1])[0]
    Save_name=f"{ckpt_name}-{time.strftime('%Y%m%d-%H%M%S')}"
    prompt["SaveImage1"]["inputs"]["filename_prefix"]= Save_name
    prompt["SaveImage2"]["inputs"]["filename_prefix"]= Save_name
    
    prompt["KSampler"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
    prompt["ImpactWildcardEncode1"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
    prompt["ImpactWildcardEncode2"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
    prompt["DetailerForEachDebug"]["inputs"]["seed"]= random.randint(0, 0xffffffffffffffff )
    
    print("prompt : ",prompt)
    queue_prompt(prompt)
    
except Exception:
    console.print_exception()
    quit()