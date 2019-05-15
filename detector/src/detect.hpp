#ifndef DETECT_H
#define DETECT_H

#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>
#include <darknet.h>
#include <string>

#include <boost/shared_ptr.hpp>
#include <boost/function.hpp>

#include <base/BlockedQueue.hpp>

#ifdef __cplusplus
extern "C"
{
#endif

    namespace CB = codechiev::base;

    using cv::Mat;
    using cv::Point;
    using cv::Rect2d;
    using cv::Scalar;
    using cv::Tracker;
    using cv::VideoCapture;

    // #include <opencv2/opencv.hpp> // wrong
    typedef cv::Ptr<Tracker> TrackerPtr;
    // typedef boost::shared_ptr<Mat> mat_ptr;
    typedef CB::BlockedQueue<1> TrafficQueue;

    struct args_t {
        network* network;
        metadata *metadata; 
        const char * name;
        const char * url;
        float thresh;
        float hier;
        int *map;
        int relative;
        bool debug;
        float x1;
        float y1;
        float x2;
        float y2;
    };

    typedef boost::shared_ptr<args_t> args_ptr;

    typedef struct
    {
        std::string id;
        int lost;// 
        bool trackable;
        bool disabled;

        double distY;
        double distX;

        TrackerPtr ptr; 
        cv::Rect2d roi;
        cv::Rect2d last;

    } DarknetTracker;
    // namespace cv
    // {
    //     class Mat;
    // }
    image mat_to_image(cv::Mat m);
    cv::Mat image_to_mat(image im);

    typedef void (*lock_func_t)();
    typedef bool (*detect_func_t)(detection *, int);
    typedef void (*track_func_t)(int,int,int,int);
    void detect(lock_func_t, detect_func_t, track_func_t, args_t *);
    void count(DarknetTracker&, float ,float,float,float, int *);

    typedef std::vector<DarknetTracker> Trackers;
    typedef std::string str;

    
    struct extra_args_t
    {
        lock_func_t lock_func;
        detect_func_t detect_func;
        track_func_t track_func;

        // str name;
        // str url;

        TrafficQueue* queue;
    };
    

    typedef boost::function<void()> detect_functor_t;

    void collect_frame(int, const char *, args_t *, extra_args_t&);

#ifdef __cplusplus
}
#endif

#endif
