rem py -m pip install torch-directml
rem py -m pip install safetensors
rem py -m pip install PyYAML==3.10
rem py -m pip install psutil
rem py -m pip install einops
rem py -m pip install transformers
rem py -m pip install scipy
rem py -m pip install torchsde
rem py -m pip install folder_paths
rem py -m pip install ultralytics!=8.0.177
rem py -m pip install aiohttp
rem py -m pip install -r requirements.txt
rem py -m pip install kornia
rem py -m pip install ultralytics
rem py -m pip install -r ComfyUI\custom_nodes\ComfyUI-Impact-Pack\requirements.txt
rem py -m pip install -r ComfyUI\custom_nodes\ComfyUI-Manager\requirements.txt
rem py -m pip install -r ComfyUI\custom_nodes\ComfyUI-Impact-Pack\impact_subpack\requirements.txt
rem py -m pip install -r ComfyUI\custom_nodes\ComfyUI-Impact-Subpack\requirements.txt
rem py C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Impact-Pack\install.py
rem py C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Impact-Subpack\install.py

py -s ComfyUI\main.py --windows-standalone-build --directml --port 8288
REM .\python-3.10.11-embed-amd64\python.exe -m pip install torch-directml
REM .\python-3.10.11-embed-amd64\python.exe -s ComfyUI\main.py --windows-standalone-build --directml
REM .\python_embeded\python.exe -m pip install torch-directml
REM .\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --directml
pause
