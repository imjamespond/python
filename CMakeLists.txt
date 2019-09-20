CMAKE_MINIMUM_REQUIRED(VERSION 3.3)

PROJECT (test-deepstream)

FIND_PACKAGE( OpenCV 3.3 REQUIRED )

set(PKGS gstreamer-1.0)
set(LIBS /opt/nvidia/deepstream/deepstream-4.0/lib/) 
set(DS_SDK_DIR -I${DS_SDK_ROOT}/sources/includes)
link_directories (/opt/nvidia/deepstream/deepstream-4.0/lib)

execute_process(COMMAND pkg-config --libs ${PKGS} OUTPUT_VARIABLE PKG_LIBS)
execute_process(COMMAND pkg-config --cflags ${PKGS} OUTPUT_VARIABLE PKG_CFLAGS)

string(STRIP ${PKG_LIBS} PKG_LIBS)
string(STRIP ${PKG_CFLAGS} PKG_CFLAGS) 

file(GLOB sourcefiles "*.cc")

set(unit_tests "test-camera")
foreach(test ${unit_tests})
  add_executable("${test}.bin" ${sourcefiles} "tests/${test}.cc") 
  set_target_properties("${test}.bin" PROPERTIES COMPILE_FLAGS "${DS_SDK_DIR} ${PKG_CFLAGS} ${CFLAGS}" )
  target_link_libraries("${test}.bin" ${PKG_LIBS} nvdsgst_meta nvds_meta)
endforeach(test)
