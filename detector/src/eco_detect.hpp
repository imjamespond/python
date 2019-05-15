#ifndef ECO_DETECT_H
#define ECO_DETECT_H

#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>
#include <eco/eco.hpp>

#include <vector>
#include <string>

#include <boost/shared_ptr.hpp>

#include "detect.hpp"

#ifdef __cplusplus
extern "C"
{
#endif

    typedef boost::shared_ptr<eco::ECO> EcoPtr;

    typedef struct
    {
        std::string id;
        int lost;// 
        bool trackable;
        bool disabled;

        double distY;
        double distX;

        cv::Rect2f roi;
        cv::Rect2f last;

        EcoPtr eco;
    } EcoTracker;

    typedef std::vector<EcoTracker> EcoTrackers;

    void eco_detect(args_t *, extra_args_t, str, EcoTrackers *, int);
    bool eco_track(EcoTrackers &, box &, Mat &);


#ifdef __cplusplus
}
#endif

#endif
