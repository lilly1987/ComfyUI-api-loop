:REDO
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/checkpoints/2d" "U:/models/checkpoints/2d"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/checkpoints/pony" "U:/models/checkpoints/pony"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/checkpoints/xl" "U:/models/checkpoints/xl"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/loras/XL" "U:/models/loras/XL"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/loras/pony" "U:/models/loras/pony"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/loras/step" "U:/models/loras/step"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/loras" "U:/models/loras"
rem ..\python_embeded\python.exe -s  "lora del add.py" %*
rem ..\python_embeded\python.exe -s  basic_api_example.py %*
pause
goto REDO