# Activating models  
By running makemigrations, you’re telling Django that you’ve made some changes to your models  
``python manage.py makemigrations polls``  
Now, run migrate again to create those model tables in your database:  
``python manage.py migrate``  

# Setting  
TEMPLATES->DIR 改为 ``os.path.join(BASE_DIR, "static")``  
views中return ``render(request, 'dist/index.html')``  
STATICFILES_DIRS 加上 上面的  

# Darknet  
yolov3 CUDA Error: out of memory darknet: ./src/cuda.c:36: check_error: Assertion `0' failed.  
``get the line batch=64 changed to 32 in yolov3.cfg``  
**create a folder named 'darknet' at root directory** which is the same dir as mysite, then copy data, cfg into it  
get this line changed  
``names = darknet/data/coco.names``  
and **make sure django cmd is excuted at this root dir** 
