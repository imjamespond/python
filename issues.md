### core dump 内存资源不足  
batch=1  
subdivisions=1  
width=320  
height=320  

### debug  
vi Makefile, set Debug=1, make -j4
gdb ./darknet  
(gdb) r detect cfg/yolov3.cfg yolov3.weights data/dog.jpg  

### 多次尝试后只能用yolov3-tiny版本  
``./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights ./data/dog.jpg``
``-nogpu``测试无gpu

