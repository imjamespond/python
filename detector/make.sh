buildpath='./build'
cd $buildpath

curpath=`realpath ../../..`

cmake . ../src \
  -DOPENTRACKER_DIR="${curpath}/OpenTracker-master" \
  -DCODECHIEV_DIR="${curpath}/codechiev-libevent" \
  -DDARKNET_DIR="${curpath}/darknet-master" \
  -DBOOST_DIR="${curpath}/boost_1_69_0"
make -j 4
