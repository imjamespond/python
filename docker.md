sudo systemctl disable docker.socket  
sudo systemctl stop docker.socket  
sudo docker pull nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04  
sudo docker run -it --name cuda9 --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04  


mkdir /opt/cctv  
mkdir /opt/lib  
mkdir -p /opt/darknet/cfg  
mkdir -p /opt/darknet/data  

sudo docker cp ~/projects/3rdparty/darknet-master/libdarknet.so cuda9:/opt/lib  
sudo docker cp ~/projects/cctv/detector/build/libcodechiev.so cuda9:/opt/lib  
sudo docker cp ~/projects/cctv/mysite/ cuda9:/opt/cctv  
sudo docker cp ~/projects/cctv/requirements.txt cuda9:/opt/cctv  
sudo docker cp ~/projects/cctv/darknet/cfg/yolov3.cfg cuda9:/opt/darknet/cfg  
sudo docker cp ~/projects/cctv/darknet/cfg/coco-1.data cuda9:/opt/darknet/cfg  
sudo docker cp ~/projects/cctv/darknet/data/coco.names cuda9:/opt/darknet/data  
sudo docker cp ~/projects/cctv/darknet/yolov3.weights cuda9:/opt/darknet  

sudo docker cp ~/lib/ cuda9:/usr/local/lib  
echo "/opt/lib" >> /etc/ld.so.conf  
ldconfig  

apt-get update  
apt-get install python3 python3-pip  
apt-get install libgtk2.0-dev  
apt-get install libsm6 libxext6 libxrender1 libfontconfig1  
apt-get install libdc1394-22-dev libdc1394-22 libdc1394-utils  
apt-get install libavcodec-ffmpeg-extra56 libavformat-ffmpeg56 libswscale-ffmpeg3 libjasper-dev libtbb2  



pip3 install --upgrade pip  
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/  
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/  

### 运行命令  
CCTVLIB=/opt/libdarknet-path python3 ./cctv/mysite/manage.py migrate  


### 相关模型  
``ls ./darknet/``  
coco.data  coco.names  yolov3.cfg  yolov3-openimages.cfg  yolov3-spp.cfg  yolov3-tiny.cfg  yolov3-tiny.weights  yolov3-voc.cfg  yolov3.weights  
``cat coco1.data``  
names = darknet/coco.names  

### detector所需共享库    
sudo echo "/opt/libdarknet-path" >> /etc/ld.so.conf   
sudo ldconfig  
