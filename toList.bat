:REDO
..\python_embeded\python.exe -m pip install mpu
..\python_embeded\python.exe -s  "toList.py" %*
rem ..\python_embeded\python.exe -s  "lora del add.py" %*
rem ..\python_embeded\python.exe -s  basic_api_example.py %*
pause
goto REDO