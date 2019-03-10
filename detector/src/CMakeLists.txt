CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT (CodeChiev)

SET(BOOST_ROOT "${BOOST_DIR}")
FIND_PACKAGE(Boost 1.6 REQUIRED)
find_package( OpenCV 3 REQUIRED )

include_directories (${CMAKE_CURRENT_SOURCE_DIR} ${BOOST_ROOT} ${CODECHIEV_DIR} ${DARKNET_DIR}/include "/usr/local/include/python3.7m")
link_directories (${DARKNET_DIR} ${CODECHIEV_DIR}/build/base)

file(GLOB SOURCE "*.cpp")
set (LIB codechiev)
add_library (${LIB} SHARED ${SOURCE})
target_link_libraries (${LIB} darknet ${OpenCV_LIBS} ccv_base) 
