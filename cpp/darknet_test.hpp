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

    // namespace cv
    // {
    //     class Mat;
    // }
    image mat_to_image(cv::Mat m);
    cv::Mat image_to_mat(image im);

    typedef void (*callback_func)(detection *, int);
    detection *predict_image(callback_func, network *, image, int, int, float, float, int *, int, int *);
    void test(callback_func, network *, metadata *, const char *, float, float, int *, int);

    typedef struct
    {
        std::string id;
        int overlapped;// 0 for new, 1 for checking, 2 for overlapped

        TrackerPtr ptr; 
        cv::Rect2d roi;

    } DarknetTracker;

#ifdef __cplusplus
}
#endif

#endif