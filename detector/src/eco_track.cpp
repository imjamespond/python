#include <stdio.h>
// #include <vector>
// #include <string>

#include "detect.hpp"
#include "eco_detect.hpp"


bool eco_track(EcoTrackers &trackers, box &bbox, Mat &frame)
{
    double w1 = bbox.w, h1 = bbox.w * 1.65;
    h1 = bbox.h > h1 ? h1 : bbox.h;// trace the top of someone
    double x1 = bbox.x - (bbox.w * .5), x1_ = x1 + w1;
    double y1 = bbox.y - (bbox.h * .5), y1_ = y1 + h1;

    double x = 0.0f, x_ = 0.0f, w = 0.0f;
    double y = 0.0f, y_ = 0.0f, h = 0.0f;

    if (w1 > 100 || h1 > 200) //bbox too large to track
    {
        return false;
    }

    bool overlapped(false);
    for (EcoTrackers::iterator it = trackers.begin(); it != trackers.end(); it++)
    {
        EcoTracker &tracker = *it;

        if (tracker.trackable)
        {
            double w2 = tracker.roi.width, h2 = tracker.roi.height;
            double x2 = (tracker.roi.x), x2_ = (tracker.roi.x + tracker.roi.width);
            x = x2 > x1 ? x2 : x1;
            x_ = x2_ > x1_ ? x1_ : x2_;
            w = x_ - x;
            double y2 = (tracker.roi.y), y2_ = (tracker.roi.y + tracker.roi.height);
            y = y2 > y1 ? y2 : y1;
            y_ = y2_ > y1_ ? y1_ : y2_;
            h = y_ - y;

            if (h > h1 * .4 && h > h2 * .4 &&
                ((x2 > x1 && x2 < x1_ && x2_ > x1 && x2_ < x1_) || //one contains the other
                 (x1 > x2 && x1 < x2_ && x1_ > x2 && x1_ < x2_) || //one contains the other
                 (w > w1 * .7 && w > w2 * .7))) //partial overlapped
            {
                overlapped = true;

                tracker.lost = 0;
                tracker.disabled = false;

                tracker.roi.x = x1;
                tracker.roi.y = y1;
                tracker.roi.width = w1;
                tracker.roi.height = h1;
                tracker.last = tracker.roi;

                tracker.distX = 0.0f;
                tracker.distY = 0.0f;

                // create a tracker object
                tracker.eco.reset(new eco::ECO());
                // initialize the tracker
                eco::EcoParameters parameters;
                parameters.useCnFeature = false;
                tracker.eco->init(frame, tracker.roi, parameters);
                // update the tracking result
                tracker.trackable = tracker.eco->update(frame, tracker.roi);

                break;
            }
        }
    }

    if (!overlapped && trackers.size() < 8)
    {
        EcoTracker tracker;
        tracker.lost = 0; 
        tracker.disabled = false;

        tracker.roi.x = x1;
        tracker.roi.y = y1; 
        tracker.roi.width = w1;
        tracker.roi.height = h1;
        tracker.last = tracker.roi;

        tracker.distX = 0.0f;
        tracker.distY = 0.0f;

        // create a tracker object
        tracker.eco.reset(new eco::ECO());
        // initialize the tracker
        eco::EcoParameters parameters;
        parameters.useCnFeature = false;
        tracker.eco->init(frame, tracker.roi, parameters);
        // update the tracking result
        tracker.trackable = tracker.eco->update(frame, tracker.roi);

        trackers.push_back(tracker);

    }
  
}

