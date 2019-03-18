#ifndef PYTEST_H
#define PYTEST_H

#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>
#include <darknet.h>
#include <string>

#ifdef __cplusplus
extern "C"
{
#endif

    // #include <opencv2/opencv.hpp> // wrong
    typedef cv::Ptr<cv::Tracker> TrackerPtr;

    struct count_args {
        network* network;
        metadata *metadata; 
        const char * name;
        const char * url;
        float thresh;
        float hier;
        int *map;
        int relative;
        float x1;
        float y1;
        float x2;
        float y2;
    };

    typedef struct
    {
        std::string id;
        int lostCount;// 
        bool trackable;
        bool disabled;

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

    typedef bool (*on_detect_func)(detection *, int);
    typedef void (*on_track_func)(int,int,int,int);
    void detect(on_detect_func, on_track_func, count_args *);
    void countTest(DarknetTracker&, float ,float,float,float, int *);


#ifdef __cplusplus
}
#endif

#endif
