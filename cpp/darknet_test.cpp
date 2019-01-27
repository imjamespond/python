#include <stdio.h>
#include <vector>
#include <opencv2/highgui.hpp>

#include "darknet_test.hpp"
#include "libs/Time.hpp"

using cv::Point;
using cv::Rect2d;
using cv::Scalar;
using cv::Tracker;

typedef std::vector<DarknetTracker> Trackers;

detection *predict_image(callback_func detect, network *net, image im, int w, int h, float thresh, float hier, int *map, int relative, int *num)
{
    // printf("predict_image: %s, %d", a, b);

    network_predict_image(net, im);

    detection *dets = get_network_boxes(net, w, h, thresh, hier, map, relative, num);

    (*detect)(dets, *num);

    return dets;
}

void test(callback_func detect, network *net, metadata *meta,  const char *url, float thresh, float hier, int *map, int relative)
{
    cv::Mat frame;
    cv::VideoCapture vc;
    vc.open(url);

    Trackers trackers;

    int iframe(0);
    for (;;)
    {
        // wait for a new frame from camera and store it into 'frame'
        vc >> frame;

        // check if we succeeded
        if (frame.empty())
        {
            //perror("ERROR! blank frame grabbed\n");
            break;
        }
        // show live and wait for a key with timeout long enough to show images
        // cv::imshow("Live", frame);
        if (cv::waitKey(5) >= 0)
        {
            break;
        }
        
        cv::resize(frame, frame, cv::Size(frame.cols * 0.75, frame.rows * 0.75), 0, 0, CV_INTER_LINEAR);

        if (iframe % 15 == 0)
        {
            trackers.clear();

            image img = mat_to_image(frame);
            int nboxes;
            network_predict_image(net, img);
            detection *dets = get_network_boxes(net, img.w, img.h, thresh, hier, map, relative, &nboxes);
            (*detect)(dets, nboxes);

            for (int i = 0; i < nboxes; ++i)
            {
                bool nothing(true);
                for (int j(0); j < meta->classes; ++j)
                {
                    if (dets[i].prob[j] > .5f)
                    {
                        nothing = false;
                        break;
                    }
                }
                if (nothing)
                    continue; 

                box &bbox = dets[i].bbox;
                cv::circle(frame, Point((int)bbox.x, (int)bbox.y), 10.0, Scalar(0, 0, 255), 1, 8);

                DarknetTracker tracker;
                tracker.roi.x = bbox.x - (bbox.w * .5);
                tracker.roi.y = bbox.y - (bbox.h * .5);
                tracker.roi.width = bbox.w;
                tracker.roi.height = bbox.h;

                // create a tracker object
                tracker.ptr = cv::TrackerKCF::create();
                // initialize the tracker
                tracker.ptr->init(frame, tracker.roi);
                // update the tracking result
                tracker.ptr->update(frame, tracker.roi);

                trackers.push_back(tracker);
            }

            free_detections(dets, nboxes);
        }
        else
        {
            for (Trackers::iterator it = trackers.begin(); it != trackers.end(); it++)
            {
                DarknetTracker &tracker = *it;
                // update the tracking result
                tracker.ptr->update(frame, tracker.roi);
                // draw the tracked object
                rectangle(frame, tracker.roi, Scalar(255, 0, 0), 2, 1);
            }

            codechiev::base::Time::SleepMillis(300);
        }

        cv::imshow("Live", frame);
        iframe++;
    }
}
