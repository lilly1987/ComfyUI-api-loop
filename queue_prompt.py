import os, sys, glob, json, random, time, copy, string, re
sys.path.append(os.getcwd())
from ConsoleColor import print, console
from rich.progress import Progress
from urllib import request

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