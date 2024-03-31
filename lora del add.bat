:REDO
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/checkpoints/2d" "U:/models/checkpoints/2d"
..\python_embeded\python.exe -s  "lora del add.py" "../ComfyUI/models/loras" "U:/models/loras"
rem ..\python_embeded\python.exe -s  "lora del add.py" %*
rem ..\python_embeded\python.exe -s  basic_api_example.py %*
pause
goto REDO