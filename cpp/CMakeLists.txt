CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT (CodeChiev)

SET(BOOST_ROOT "${BOOST_DIR}")
FIND_PACKAGE(Boost 1.6 REQUIRED)
find_package( OpenCV 3 REQUIRED )

include_directories (${CMAKE_CURRENT_SOURCE_DIR}/darknet/include ${BOOST_ROOT} "/usr/local/include/python3.7m")
link_directories (${CMAKE_CURRENT_SOURCE_DIR}/darknet ${CMAKE_CURRENT_SOURCE_DIR}/libs)

file(GLOB SOURCE "*.cpp")
set (LIB codechiev)
add_library (${LIB} SHARED ${SOURCE})
target_link_libraries (${LIB} darknet ${OpenCV_LIBS} ccv_base) 

SET (UnitTest camera_test)
add_executable (${UnitTest} ${UnitTest}.cpp)
target_link_libraries (${UnitTest} opencv_core)
add_test(${UnitTest} ${CMAKE_CURRENT_BINARY_DIR}/${UnitTest})
