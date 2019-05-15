#include <base/Logger.hpp>
#include <base/Time.hpp>

#include <opencv2/opencv.hpp>

using namespace cv;
namespace CB = codechiev::base;

void collect_frame(int, const char *);

int main(int argc, char **argv)
{
  if (argc > 1) 
  {
    LOG_INFO << "video: " << argv[1];
    
    VideoCapture vc;
    vc.open(argv[1]);

    Mat frame;
    int num(0);
    for (;;)
    {
      // wait for a new frame from camera and store it into 'frame'
      vc >> frame;
      // check if we succeeded
      if (frame.empty())
      {
        LOG_ERROR << "ERROR! blank frame grabbed";

        vc.release();
        vc.open(argv[1]);

        // check if we succeeded
        if (!vc.isOpened())
        {
          LOG_ERROR << "ERROR! camera is closed";
        }

        CB::Time::SleepMillis(1000L);
        continue;
      }

      LOG_INFO << "frame: " << num;

      cv::resize(
        frame, frame, 
        cv::Size(320.0f, (int)(320.0f / (float)frame.cols * (float)frame.rows)), 
        0, 0, CV_INTER_LINEAR);

      // show live and wait for a key with timeout long enough to show images
      imshow("Live", frame);
      if (waitKey(50) >= 0)
        break;

      if (++num >= 1000)
      {
        num = 0;
      }
    }
  }
  else
  {
    LOG_INFO << "must add a video parameter!";
  }

}
