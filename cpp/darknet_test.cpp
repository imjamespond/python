#include <stdio.h>
#include <vector>
#include <opencv2/highgui.hpp>
#include <boost/lexical_cast.hpp>

#include "darknet_test.hpp"
#include "libs/Time.hpp"

using cv::Mat;
using cv::Point;
using cv::Rect2d;
using cv::Scalar;
using cv::Tracker;
using cv::VideoCapture;

typedef std::vector<DarknetTracker> Trackers;

bool __check_overlapped__(Trackers &, box &, Mat &, int &);
void __clean_trackers__(Trackers &);

detection *predict_image(callback_func detect, network *net, image im, int w, int h, float thresh, float hier, int *map, int relative, int *num)
{
    // printf("predict_image: %s, %d", a, b);

    network_predict_image(net, im);

    detection *dets = get_network_boxes(net, w, h, thresh, hier, map, relative, num);

    (*detect)(dets, *num);

    return dets;
}

void test(callback_func detect, network *net, metadata *meta, const char *url, float thresh, float hier, int *map, int relative)
{
    Mat frame;
    VideoCapture vc;
    vc.open(url);

    Trackers trackers;

    int iframe(0);
    int count(0);
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

        for (Trackers::iterator it = trackers.begin(); it != trackers.end(); it++)
        {
            DarknetTracker &tracker = *it;
            if (tracker.overlapped > 1) 
            {
                continue;
            }

            // update the tracking result
            tracker.trackable = tracker.ptr->update(frame, tracker.roi);
            // draw the tracked object
            cv::rectangle(frame, tracker.roi, Scalar(255, 0, 0), 2, 1);
            cv::putText(frame,
                        tracker.id,
                        Point(tracker.roi.x, tracker.roi.y), // Coordinates
                        cv::FONT_HERSHEY_COMPLEX_SMALL,      // Font
                        1.0,                                 // Scale. 2.0 = 2x bigger
                        Scalar(255, 255, 255)                // BGR Color
            );
        }

        if (iframe % 15 == 0)
        {
            // trackers.clear();

            image img = mat_to_image(frame);
            int nboxes;
            network_predict_image(net, img);
            detection *dets = get_network_boxes(net, img.w, img.h, thresh, hier, map, relative, &nboxes);
            (*detect)(dets, nboxes);

            for (int i = 0; i < nboxes; ++i)
            {
                bool nothing(true);
                // for (int j(0); j < meta->classes; ++j)
                for (int j(0); j < 1; ++j) // detect people only
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
                __check_overlapped__(trackers, bbox, frame, count);
            }
            __clean_trackers__(trackers);

            free_image(img);
            free_detections(dets, nboxes);
        }
        else
        {

            codechiev::base::Time::SleepMillis(300);
        }

        cv::imshow("Live", frame);
        iframe++;
    }
}

bool __check_overlapped__(Trackers &trackers, box &bbox, Mat &frame, int &count)
{
    double w1 = bbox.w, h1 = bbox.h;
    double x1 = bbox.x - (bbox.w * .5), x1_ = x1 + w1;
    double y1 = bbox.y - (bbox.h * .5), y1_ = y1 + h1;

    double x = 0.0f, x_ = 0.0f, w = 0.0f;
    double y = 0.0f, y_ = 0.0f, h = 0.0f;
    
    bool overlapped(false);
    for (Trackers::iterator it = trackers.begin(); it != trackers.end(); it++)
    {
        DarknetTracker &tracker = *it;

        double w2 = tracker.roi.width, h2 = tracker.roi.height;
        double x2 = (tracker.roi.x), x2_ = (tracker.roi.x + tracker.roi.width);
        x = x2 > x1 ? x2 : x1;
        x_ = x2_ > x1_ ? x1_ : x2_;
        w = x_ - x;
        double y2 = (tracker.roi.y), y2_ = (tracker.roi.y + tracker.roi.height);
        y = y2 > y1 ? y2 : y1;
        y_ = y2_ > y1_ ? y1_ : y2_;
        h = y_ - y;

        if (w/w1>.8 && w/w2>.8 && h/h1>.4 && h/h2>.4)
        {
            //tracker and detection of darknet overlapped
            printf("%f, %f\n", w, h);
            overlapped = true;
            tracker.overlapped = 0;

            tracker.roi.x = x1;
            tracker.roi.y = y1;
            tracker.roi.width = w1;
            tracker.roi.height = h1;

            if (!tracker.trackable)
            {
                // create a tracker object
                tracker.ptr = cv::TrackerKCF::create();
                // initialize the tracker
                tracker.ptr->init(frame, tracker.roi);
                // update the tracking result
                tracker.ptr->update(frame, tracker.roi);
            }


            break;
        }
    }

    if (!overlapped)
    {
        DarknetTracker tracker;
        tracker.id = boost::lexical_cast<std::string>(++count);
        tracker.overlapped = 0; 

        tracker.roi.x = x1;
        tracker.roi.y = y1;
        tracker.roi.width = w1;
        tracker.roi.height = h1;

        // create a tracker object
        tracker.ptr = cv::TrackerKCF::create();
        // initialize the tracker
        tracker.ptr->init(frame, tracker.roi);
        // update the tracking result
        tracker.trackable = tracker.ptr->update(frame, tracker.roi);

        trackers.push_back(tracker);

	printf("count: %d\n",count);
    }
  
}

void __clean_trackers__(Trackers &trackers)
{
    for (Trackers::iterator it = trackers.begin(); it != trackers.end(); )
    {
        DarknetTracker &tracker = *it;

        if (tracker.overlapped > 3)
        {
            it = trackers.erase(it);
        }
        else
        {
            tracker.overlapped += 1; // deletable in next round
            it++;
        }
        
    }
}
