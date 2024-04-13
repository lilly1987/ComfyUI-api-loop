import os, sys, glob, random, time, copy, string, re, numbers
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

if len(sys.argv) < 2:
    c=input("char : ")
    if len(c)==0:
        print("[red] input 0 ")
        sys.exit()
    cl=[c]
    
else:
    print("argv :", sys.argv)
    cl=sys.argv[1:]
    #sys.exit()
print("cl :", cl)
    

fm={
    "loras":{
    },
    "lorasUpdate":False,
}

xl=[
            #insertions
            "LargeInsertion-v1",
            "ridingDildoSexActLora_v11",
            "haraboko_v3",
            "DbDildo",
            "DildoRiding",
            "arm_grab_doggy",
            "monsterSexActLora79_v10",
            "koonagoConcept_v1",
            "hyper_penetration_stomach_bulge_v8pectoral",
            "hyper_penetration_stomach_bulge_v8absurd",
            "hyper_penetration_stomach_bulge_v8nice",
            "hyper_penetration_stomach_bulge_v8all",
            "huge_dildo_v1_goofy",
            "Large_object_insertions-000009",
            "lactation egg-001",
            "conceptLargerInsertion_v10",
            "raised-doggystyle-v3-wasabiya",
            #bdsm
            "boundsittinglegstogether-03",
            "bdsm_v3",
            "bdsm_frame",
            "bdsm_pissoir-000002",
            "BondagePoleV1",
            "Luoxuan_V2",
            "Armbinder",
            #Deepthroat
            "GloryHolev2 1024-000048",
            "side-deepthroat-v3-wasabiya",
            "side-fellatio-b3-v3-wasabiya",
            "osofel",
            "Deepthroat",
            "ddkb_v1",
            "hugandSuckConcept_v1",
            "SideFellatio",
            "X-ray Fellatio 1.5_1-000042",            
            #obp
            "obp-000050",
            #hang
            "execution_on_gallows",
            "aki",
            "aki-000012",
            "aki-000014",
            "aki-000018",
            "aki-000020",
            "aki-000024",
            "hunged_girl",
            "leheng_re",
            "hang",
            #transformation
            "transformation",
            "sex_toy_transformation",
            "onahole_personality_v17",
]


print(os.getcwd())

for c in cl :
    for x in xl :
        fm["loras"]["char"]=c
        fm["loras"]["xxx"]=x
        print(c,x)
        print(fm)
        fn=f"tmp/{c}-{x}.json"
        mpu.io.write(fn, fm)
        #with open(fn, 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(fm,indent="\t"))