buildpath='./build'
cd $buildpath

cmake . ../src \
  -DCODECHIEV_DIR="/home/james/projects/3rdparty/codechiev-libevent" \
  -DDARKNET_DIR="/home/james/projects/3rdparty/darknet-master" \
  -DBOOST_DIR="/home/james/projects/3rdparty/boost_1_69_0"
make -j 4
