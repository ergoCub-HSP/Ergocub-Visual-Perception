# ErgoCub-Visual-Perception

## Checkpoints and Assets
Download the following archive and place the assets following the indications in the README. [Link](https://istitutoitalianotecnologia-my.sharepoint.com/:f:/g/personal/andrea_rosasco_iit_it/EluMY5FLUC1FqMI_u4T4NB8B1zKwYWmiuCmYOPSmD9n6xA?e=L2wX4Z)
### Conda
- [Cuda 11.4.4](https://developer.nvidia.com/cuda-11-4-4-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local) (filename `cuda_11.4.4_472.50_windows.exe`, fourth update)
- [CUDNN 8.2.1](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/8.2.1.32/11.3_06072021/cudnn-11.3-windows-x64-v8.2.1.32.zip) (filename `cudnn-11.3-windows-x64-v8.2.1.32.zip`)
- [TensorRT 8.2.3.0](https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/8.2.3.0/zip/TensorRT-8.2.3.0.Windows10.x86_64.cuda-11.4.cudnn8.2.zip) (filename `TensorRT-8.2.3.0.Windows10.x86_64.cuda-11.4.cudnn8.2.zip`, second update)
### Docker
The docker image is available at `andrew/ecub_env:latest`, or you can build it with:

`docker build -t ecub .`

You can launch the bash of the docker's image with access to the GPUs and also mounting the actual path with the following command

`docker run -it --rm --gpus=all -v "%cd%":/home/ecub ecub:latest /bin/bash`
## To run everything
The engines are already contained inside the repository thanks to Git-LFS.
You can find the engines also inside the release, or you can rebuild them on your machine.
From the root directory (not inside docker):

`python scripts/manager.py`

`python scripts/source.py`

`python scripts/sink.py`

From the root directory (inside the docker):

`python scripts/grasping_pipeline.py`

From the ISBFSAR directory (inside the docker (you may have to set the PYTHONPATH)):

`PYTHONPATH="/home/ecub/ISBFSAR"; python ISBFSAR/main.py`
