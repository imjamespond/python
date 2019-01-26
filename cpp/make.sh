buildpath='build'

mkdir -p $buildpath
cd $buildpath

cmake . .. \
  -DBOOST_DIR="/home/james/projects/3rdparty/boost_1_69_0"
make -j 4
