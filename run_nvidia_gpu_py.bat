rem conda --help
rem conda search --full-name python
rem conda create -n py3.10.14 python=3.10.14
rem conda activate py3.10.14
rem pip install torch-directml
rem pip install safetensors
rem pip install yaml
rem pip install psutil
rem pip install einops
rem pip install transformers
rem pip install scipy
rem pip install torchsde
rem pip install aiohttp
rem pip install kornia
rem pip install segment_anything
rem pip install cv2
C:\Users\lilly\AppData\Local\miniconda3\envs\py3.10.14\python.exe -s ComfyUI\main.py --windows-standalone-build --directml --port 8288  --lowvram --use-split-cross-attention

REM .\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --directml --use-split-cross-attention --force-fp16 --fp16-unet --fp16-vae
pause

rem py -m pip install -r ComfyUI\requirements.txt
rem py -m pip install -r ComfyUI\custom_nodes\ComfyUI-Impact-Pack\requirements.txt
rem py -m pip install -r ComfyUI\custom_nodes\ComfyUI-Manager\requirements.txt
rem py -m pip install torch-directml

rem py -s ComfyUI\main.py --windows-standalone-build --directml --port 8288  --lowvram --use-split-cross-attention

rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\requirements.txt
rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Impact-Pack\requirements.txt
rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Impact-Pack\impact_subpack\requirements.txt
rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Impact-Subpack\requirements.txt
rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Inspire-Pack\requirements.txt
rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Manager\requirements.txt
rem pip install -r C:\ComfyUI_windows_portable\ComfyUI\requirements.txt
