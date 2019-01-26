#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <darknet.h>

#include "darknet_test.hpp"

detection *predict_image(callback_func detect, network *net, image im, int w, int h, float thresh, float hier, int *map, int relative, int *num )
{
    // printf("predict_image: %s, %d", a, b);

    network_predict_image(net, im);

    detection *dets = get_network_boxes(net, w, h, thresh, hier, map, relative, num);

    (*detect)(dets, *num); 
    
    return dets;
}

void test(callback_func detect, network *net, const char *url,float thresh, float hier, int *map, int relative)
{
    cv::Mat frame;
    cv::VideoCapture vc;
    vc.open(url);

    for (;;)
    {
        // wait for a new frame from camera and store it into 'frame'
        vc >> frame;

        // check if we succeeded
        if (frame.empty())
        {
            perror("ERROR! blank frame grabbed\n");
            break;
        }
        // show live and wait for a key with timeout long enough to show images
        cv::imshow("Live", frame);
        if (cv::waitKey(5) >= 0)
        {
            break;
        }

        image img = mat_to_image(frame);
        int num;
        network_predict_image(net, img);
        detection *dets = get_network_boxes(net, img.w, img.h, thresh, hier, map, relative, &num);
        (*detect)(dets, num); 
    }
}
