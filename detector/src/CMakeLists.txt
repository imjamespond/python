CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT (CodeChiev)

SET(BOOST_ROOT "${BOOST_DIR}")
FIND_PACKAGE(Boost 1.6 REQUIRED)
FIND_PACKAGE( OpenCV 3.4 REQUIRED )

include_directories (${CMAKE_CURRENT_SOURCE_DIR} ${OPENTRACKER_DIR} ${BOOST_ROOT} ${CODECHIEV_DIR}/codechiev ${DARKNET_DIR}/include "/usr/local/include/python3.7m")
link_directories (${DARKNET_DIR} ${OPENTRACKER_DIR}/eco ${CODECHIEV_DIR}/build/base)

file(GLOB SOURCE "*.cpp")
set (LIB codechiev)
add_library (${LIB} SHARED ${SOURCE})
target_link_libraries (${LIB} darknet ecotracker ${OpenCV_LIBS} ccv_base pthread) 

add_executable(test-ecotracker.bin ${SOURCE} "tests/test-ecotracker.cc")
target_link_libraries (test-ecotracker.bin darknet ecotracker ${OpenCV_LIBS} ccv_base pthread) 

add_executable(test-collect-frame.bin ${SOURCE} "tests/test-collect-frame.cc")
target_link_libraries (test-collect-frame.bin  darknet ecotracker ${OpenCV_LIBS} ccv_base pthread) 