import os, sys, glob, random, time, copy, string, re, numbers
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from JoinLib import *
from fileRead import *
from updateLib import *
from queue_prompt import *
from GetLib import *
from minmax import *
#sys.path.append("../ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact")
#import wildcards


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
    


#with console.status("[bold green]Working on tasks...") as status:

ckptCnt=0
ckptMax=0
jitemCnt=0
jitemMax=0
tm=time.strftime('%Y%m%d-%H%M%S')
logFile=f"log/{tm}.html"
while True:
    try:
        setup=dicFileRead("setup.json")
        ccolor=setup["ccolor"]
        #print("setup : ",setup)
        
        # -------------------------------------------------
        cuda=torch.cuda.is_available()
        #print(f"[{ccolor}]cuda : [/{ccolor}]",cuda)
        if cuda and "cuda" in setup:
            dupdate(setup,setup["cuda"])
        elif not cuda and "cpu" in setup:
            dupdate(setup,setup["cpu"])
            

        
        # -------------------------------------------------
        if jitemCnt<=0:
            
            jlist=getFileList("list/**/*.json")
            #print("jlist1 : ",jlist)
            
            listMatchs=setup.get("listMatch",["*"])
            if len(listMatchs)==0:
                print("[red] no listMatchs : [/red]", listMatchs)
                listMatchs=["*"]
            
            listMatch=random.choice(listMatchs)
            #print("listMatch : ",listMatch)
            
            jlist=[ i for i in jlist if i.match(f"list/{listMatch}.json")]
            #print("jlist2 : ",jlist)
            if len(jlist)==0:
                print("[red] no jlist : [/red]", listMatch)
                continue
            
            jchoice=random.choice(jlist)
            print("jchoice : ",jchoice)
            jitem=dicFileRead(jchoice)
            jitem_name=os.path.splitext(os.path.split(jchoice)[1])[0]
            
            #print("jitem_name : ",jitem_name)
            
            jitemMax=jitemCnt=setup.get("itemCnt",8)
            
        
        dupdate(setup,jitem)
        
        # -------------------------------------------------
        if ckptCnt<=0:
            
            if random.random() < setup.get("ckptPer",0) :
                ckpt_path=setup["ckptPathSplit"]+"**/"+random.choice(dicFileRead("ckpt.json"))+".safetensors"
            else:
                ckpt_path=setup["ckptPath"]
            
            ckptList=getFileList(ckpt_path)
            if  isinstance(ckptList, list) and len(ckptList)>0:
                ckpt_path=random.choice(ckptList)
            else:
                print("[res]ckpt_path[/res] : ",ckpt_path)
                continue
            ckpt_path=pathRemove(ckpt_path,setup["ckptPathSplit"])
            
            ckptMax=ckptCnt=setup.get("ckptCnt",8)
            
            print("ckpt_path : ",ckpt_path)
            ckpt_name=os.path.splitext(os.path.split(ckpt_path)[1])[0]
            
            vaeList=getFileList(setup["vaePath"])
            vae_path=random.choice(vaeList)
            vae_path=pathRemove(vae_path,setup["vaePathSplit"])
            vae_name=os.path.splitext(os.path.split(vae_path)[1])[0]
            #print("vae_path  : ",vae_path)
            
        
        # -------------------------------------------------
        
        prompt=jsonFileRead(setup.get("workflow","workflow_api.json"))
            
        # -------------------------------------------------
        
        loras=dicFileRead("loras.json")
        if setup.get("lorasUpdate",True):
            dupdate(setup["loras"],loras)
        
        #lorasDic=dicFileRead("lorasDic.json")
        lorasDic=dicFilesRead("lorasDics/*.json")
        #print("lorasDics  : ",lorasDic)
        dupdate(setup["lorasDic"],lorasDic)
        
        lbw=dicFileRead("lbw.json")
        # -------------------------------------------------
        #prompt["LoraLoader"]["inputs"]["lora_name"]=""
        #aLora=copy.deepcopy(prompt["LoraLoader"])
        loraList=getFileList(setup["loraPath"]+"**/*.safetensors")
        
        tchoice=random.choice(loraList)
        tname=pathRemove(tchoice,setup["loraPath"])
        lora1="CheckpointLoaderSimple"
        lora2="LoraLoader"
        prompt[lora2]["inputs"]["lora_name"]=tname
        prompt[lora2]["inputs"]["strength_model"]=0
        prompt[lora2]["inputs"]["strength_clip"]=0
        
        print("loraList : ",len(loraList))
        
        for k, v in setup.get("loras",{}).items():
            #print(f"{k} : ", v)
            try:
                tmp=v
                #print(f"loras : tmp : ", tmp)
                #-----------------------------
                if isinstance(tmp, str) :
                    tmp=lorasDic.get(tmp)
                    if isinstance(tmp, list):
                        tmp=random.choice(tmp)
                        tmp=lorasDic.get(tmp)
                    if tmp is None:
                        print(f"loras :[red] None1 {k} : [/red]", v)
                        continue
                if setup.get("lora show"):
                    print(f"loras :[cyan] {k} : [/cyan]", v)
                    #setup["loras"][k]=glora
                if isinstance(tmp, tuple) :
                    if isinstance(tmp[0], numbers.Number) :
                        if minmaxft(tmp[0]) > random.random() :
                            tmp=tmp[1]
                        else:
                            if setup.get("skip show",False) :
                                print(f"loras :[yellow] {k} skip [/yellow]")
                            continue
                    #else:
                    #    print(f"loras :[yellow] {k} not num [/yellow]")
                else:
                    print(f"loras :[red]no tuple  {k} : [/red]", v)
                    continue
                #-----------------------------
                tmp2=tmp
                if isinstance(tmp2, list):
                    tmp3=random.choice(tmp2)
                else:
                    tmp3=tmp2
                if tmp3 is None:
                    print(f"loras :[red] None2 {k} : [/red]", v)
                    print(f"loras :[red] None2 {k} : [/red]", tmp2)
                    print(f"loras :[red] None2 {k} : [/red]", tmp3)
                    continue
                if isinstance(tmp3, str):
                    tmp4=lorasDic.get(tmp3)
                else:
                    tmp4=tmp3
                if tmp4 is None:
                    print(f"loras :[red] None3 {k} : [/red]", v)
                    print(f"loras :[red] None3 {k} : [/red]", tmp3)
                    print(f"loras :[red] None3 {k} : [/red]", tmp4)
                    continue
                #-----------------------------
                tmp=tmp4
                #print("tmp4 : ",tmp)
                if isinstance(tmp, list):
                    tmp5=random.choice(tmp)
                    tmp=lorasDic.get(tmp5)
                if isinstance(tmp[0], list):
                    vl=random.choice(tmp[0])
                    print(f"loras :[green] list {k} : [/green]", tmp[0])
                elif isinstance(tmp[0], str):
                    vl=tmp[0]
                else:
                    print(f"loras :[red] unknown {k} : [/red]", vl)
                    continue
                    
                #print("loraList : ",loraList)
                tloraList=[ i for i in loraList if i.match(f"{vl}.safetensors")]
                if len(tloraList)==0:
                    print("[red] no loraList : [/red]",vl)
                    continue
                
                tchoice=random.choice(tloraList)
                tname=pathRemove(tchoice,setup["loraPath"])
                print(f"loras : [green]{tname}[/green]")
                
                tLora=copy.deepcopy(prompt[lora2])
                tLora["inputs"]["lora_name"]=tname
                tLora["inputs"]["strength_model"]=minmaxft(tmp[1])
                tLora["inputs"]["strength_clip"]=minmaxft(tmp[2])
                tLora["inputs"]["model"][0]=lora1
                tLora["inputs"]["clip"][0]=lora1
                if len(tmp) >5 :
                    t5=tmp[5]
                    if isinstance(t5, list):
                        t5=random.choice(t5)
                    if  isinstance(t5, str) :
                        if "rnd" == t5.lower() : 
                            t5=random.choice(list(lbw.values()))
                        else:
                            t5=lbw.get(t5.upper(),t5)
                        tLora["inputs"]["block_vector"]=t5
                        print("[green] t5 : [/green]",t5)
                    else:
                        print("[red] no str t5 : [/red]",t5)
                
                lora1=f"LoraLoader-{k}"
                prompt[lora1]=tLora
                prompt[lora2]["inputs"]["model"][0]=lora1
                prompt[lora2]["inputs"]["clip"][0]=lora1
                
                dupdate(setup["positive"],tmp[3])
                if len(tmp) >4 :
                    dupdate(setup["negative"],tmp[4])
                
            except Exception:
                #console.print_exception(show_locals=True)
                print("tmp : ",tmp)
                console.print_exception()
        #print("setup : ",setup)
        #print("prompt : ",prompt)
        
        dupdate(setup,jitem)
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
        type="EmptyLatentImage"

        promptSetInt(prompt,setup,type,"width")
        promptSetInt(prompt,setup,type,"height")
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
        tm=time.strftime('%Y%m%d-%H%M%S')
        # Save_name=f"{ckpt_name}-{time.strftime('%Y%m%d-%H%M%S')}"
        
        if setup.get("SaveImage1",True):
            sampler_name1=prompt["KSampler"]["inputs"]["sampler_name"]
            scheduler1=prompt["KSampler"]["inputs"]["scheduler"]
            cfg1=int(prompt["KSampler"]["inputs"]["cfg"])
            prompt["SaveImage1"]["inputs"]["filename_prefix"]= f"{ckpt_name}/{jitem_name}/{ckpt_name}-{sampler_name1}-{scheduler1}-{cfg1}-{jitem_name}-{tm}"
            print(f"{ckpt_name}-{sampler_name1}-{scheduler1}-{cfg1}-{jitem_name}-{tm}")
        else:
            del prompt["SaveImage1"]
            
        if setup.get("SaveImage2",True):
            sampler_name1=prompt["DetailerForEachDebug"]["inputs"]["sampler_name"]
            scheduler1=prompt["DetailerForEachDebug"]["inputs"]["scheduler"]
            cfg1=int(prompt["DetailerForEachDebug"]["inputs"]["cfg"])
            #prompt["SaveImage2"]["inputs"]["filename_prefix"]= f"{ckpt_name}/{sampler_name1}/{scheduler1}/{cfg1}/{jitem_name}/{ckpt_name}-{sampler_name1}-{scheduler1}-{cfg1}-{jitem_name}-{tm}"
            prompt["SaveImage2"]["inputs"]["filename_prefix"]= f"{ckpt_name}/{jitem_name}/{ckpt_name}-{sampler_name1}-{scheduler1}-{cfg1}-{jitem_name}-{tm}"
            print(f"{ckpt_name}-{sampler_name1}-{scheduler1}-{cfg1}-{jitem_name}-{tm}")
        else:
            del prompt["SaveImage2"]
        
        # -------------------------------------------------
        s=setup.get("textJoin",", BREAK ")
        type="positiveWildcard"
        promptSetInt(prompt,setup,type,"seed",random.randint(0, 0xffffffffffffffff ))
        prompt[type]["inputs"]["wildcard_text"]= textJoin(
                setup["positive"],
                shuffle=setup.get("shufflepositive",setup.get("shuffle",False)),
                s=s
        )

        # -------------------------------------------------
        type="negativeWildcard"
        promptSetInt(prompt,setup,type,"seed",random.randint(0, 0xffffffffffffffff ))
        prompt[type]["inputs"]["wildcard_text"]= textJoin(
                setup["negative"],
                shuffle=setup.get("shufflenegative",setup.get("shuffle",False)),
                s=s
        )
        
        
        # -------------------------------------------------
       
        
        #prompt["ImpactWildcardEncode2"]["inputs"]["wildcard_text"]= wildcards.process(textJoin(
        #        setup["negative"],
        #        shuffle=setup.get("shufflenegative",setup.get("shuffle",False))
        #    ), prompt["ImpactWildcardEncode2"]["inputs"]["seed"])
        #    
        #prompt["ImpactWildcardEncode1"]["inputs"]["wildcard_text"]= wildcards.process(textJoin(
        #        setup["positive"],
        #        shuffle=setup.get("shufflepositive",setup.get("shuffle",False))
        #    ),  prompt["ImpactWildcardEncode1"]["inputs"]["seed"])
        # -------------------------------------------------
        
        if setup.get("jitem show"):
            print("jitem : ",jitem)
        if setup.get("setup show"):
            print("setup : ",setup)
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
    except KeyboardInterrupt:
        print('Interrupted')
        console.save_html(logFile)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
    except Exception:
        #console.print_exception(show_locals=True)
        console.print_exception()
        #console.save_html(logFile)
        #quit()
    # -------------------------------------------------
    ckptCnt-=1
    jitemCnt-=1
    # -------------------------------------------------