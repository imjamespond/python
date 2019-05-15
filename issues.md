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

### compile and install opencv3.4 then remove jetson nano opencv3.3  
sudo mv /usr/lib/libopencv* /somewhere  
sudo ldconfig  

### OSError: libdarknet.so: cannot open shared object file: No such file or directory  
File "/home/apollo/projects/cctv/mysite/cctv/darknet.py", line 74, in <module>  
    libcodechiev = CDLL(os.environ['CCTVLIB'] + "/libcodechiev.so", RTLD_GLOBAL)  
``sudo vim.basic /etc/ld.so.conf``  
add /home/appollo/projects/darknet-master  
add 
``sudo ldconfig``  

### OSError: /home/apollo/projects/libs/libcodechiev.so: undefined symbol: _ZN2cv7Tracker6updateERKNS_11_InputArrayERNS_5Rect_IdEE  
1, 具体原因不清, 重新完整编译opencv即可, 估计是opencv库拷过来时不全  
2, 可能是link时没将.so加入target_link_libraries, 导致找不到定义

### ***libccv_base.a(Thread.cpp.o): relocation R_AARCH64_ADR_PREL_PG_HI21 against symbol `_ZTTN5boost10wrapexceptINS_17bad_function_callEEE' which may bind externally can not be used when making a shared object; recompile with -fPIC  
codechiev项目加上 SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall ``-fPIC``")  

### /usr/bin/ld: cannot find -ldarknet
注意link时用的是库也可以是 .so, 因此要将.so加入``link_directories``   
