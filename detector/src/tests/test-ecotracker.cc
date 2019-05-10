#include <base/Logger.hpp>
#include <base/Time.hpp>

#include <eco/eco.hpp>
#include <opencv2/opencv.hpp>

using cv::Mat;
using cv::Rect2d;
using cv::Rect2f;
using cv::Scalar;
using cv::VideoCapture;

void test_eco(const char *);

int main(int argc, char **argv)
{
  if (argc > 1) 
  {
    LOG_INFO << "video: " << argv[1];
    test_eco(argv[1]);
  }
  else
  {
    LOG_ERROR << "must add a video parameter!";
  }
 
}

void test_eco(const char *video_source)
{
  /* 无法判断追踪失败
  this is a short-term tracking algorithm, 
  do not have mechanism to judge failure, 
  you can add similarity ,distance to all cluster center or other methods 
  */
  eco::ECO ecotracker;
  eco::EcoParameters parameters;

  VideoCapture vc;
  Mat frame;
  Rect2f ecobbox;

  vc.open(video_source);

  for (;;)
  { 
    vc >> frame; 
    if (frame.empty())
    { 
      break;
    }

    Mat _frame;
    cv::resize(frame, _frame, cv::Size(640.0f, (int)(640.0f / (float)frame.cols * (float)frame.rows)), 0, 0, CV_INTER_LINEAR);

    //https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=waitkey
    //This function should be followed by waitKey function which displays the image for specified milliseconds
    // cv::imshow("test-win", _frame);
    int key = cv::waitKey(100);
    if (key >= 0)
    {
      if (key == 'q')
      {
        LOG_INFO << key;
        break;
      }
      else if (key == 's')
      {
        ecobbox = cv::selectROI("test-win", _frame, false, false);

        parameters.useCnFeature = false;

        ecotracker.init(_frame, ecobbox, parameters);
      }
    }

    bool okeco = ecotracker.update(_frame, ecobbox);

    if (okeco)
    {
      cv::rectangle(_frame, ecobbox, Scalar(255, 0, 0), 2, 1);
    }

    cv::imshow("test-win", _frame);
  }
}