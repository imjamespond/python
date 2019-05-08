buildpath='./build'
cd $buildpath

cmake . ../src \
  -DCODECHIEV_DIR="../../../codechiev-libevent" \
  -DDARKNET_DIR="../../../darknet-master" \
  -DBOOST_DIR="../../../boost_1_69_0"
make -j 4
