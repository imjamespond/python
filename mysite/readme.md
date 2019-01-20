# Activating models  
By running makemigrations, you’re telling Django that you’ve made some changes to your models  
``python manage.py makemigrations polls``  
Now, run migrate again to create those model tables in your database:  
``python manage.py migrate``  


# Darknet  
yolov3 CUDA Error: out of memory darknet: ./src/cuda.c:36: check_error: Assertion `0' failed.  
``have the line batch=64 changed to 32 in yolov3.cfg``  
create a folder named 'darknet' at root directory, the same dir as mysite, then copy data, cfg to it  
get this line changed  
``names = darknet/data/coco.names``  
