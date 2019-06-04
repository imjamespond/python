#include "eco_detect.hpp"

#include <base/Logger.hpp>
#include <base/Time.hpp>

#include <boost/bind.hpp>
#include <boost/lexical_cast.hpp>
#include <vector>
#include <stdio.h>

#define PATH "/tmp/traffic-cache/"

void openvc(VideoCapture &vc, const char *url)
{
  vc.open(url, cv::CAP_GSTREAMER);
}

void collect_frame(int queue_max_size, const char * url, args_t * args, extra_args_t& extra_args)
{
  const char *mkdir = "mkdir -p " PATH;
  ::system(mkdir);

  extra_args.queue->start();

  // Mat frame;
  VideoCapture vc;
  openvc(vc, url);

  int num(0);
  bool running(true);

  EcoTrackers trackers;

  Mat frame;
  for (;;)
  {

    // wait for a new frame from camera and store it into 'frame'
    vc >> frame;

    if (frame.empty())
    {
      LOG_ERROR << "ERROR! blank frame grabbed";

      vc.release();
      openvc(vc, url);

      // check if we succeeded
      if (!vc.isOpened())
      {
        LOG_ERROR << "ERROR! camera is closed";
      }

      CB::Time::SleepMillis(500L);
      continue;
    }

    cv::resize(frame, frame, cv::Size(640.0f, (int)(640.0f / (float)frame.cols * (float)frame.rows)), 0, 0, CV_INTER_LINEAR);

    // int64_t now = codechiev::base::Time::Now().getMillis();
    str frameFile = PATH;
    frameFile += boost::lexical_cast<str>(num) + ".png";

    std::vector<int> compression_params;
    compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
    compression_params.push_back(5);

    try {
      cv::imwrite(frameFile, frame, compression_params);
    }
    catch (std::runtime_error& ex) 
    {
        LOG_ERROR << "Exception converting image to PNG format: " << ex.what();
        break;
    }

    int size = extra_args.queue->size();
    if (size < queue_max_size && running)
    {
      detect_functor_t detect_functor = boost::bind(&eco_detect, args, extra_args, frameFile, &trackers, num);
      if (!extra_args.queue->add(detect_functor))
        break;

      if (++num >= queue_max_size)
      {
        num = 0;
      }
    }
    else
    {
      if (size < (queue_max_size >> 1))
      {
        running = true;
      }
      else
      {
        running = false;

        LOG_DEBUG << "queue size reach limit: " << size;
        CB::Time::SleepMillis(1000L);
      }

      continue;
    }

    // CB::Time::SleepMillis(25L);
  }

  extra_args.queue->join();

  vc.release();

  if (args->debug)
  {
    cv::destroyAllWindows();
  }

  LOG_INFO << "total frame: " << num;
}
