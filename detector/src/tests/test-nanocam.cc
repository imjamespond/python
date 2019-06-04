// simple_camera.cpp
// MIT License
// Copyright (c) 2019 JetsonHacks
// See LICENSE for OpenCV license and additional information
// Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
// NVIDIA Jetson Nano Developer Kit using OpenCV
// Drivers for the camera and OpenCV are included in the base image

// #include <iostream>
#include <opencv2/opencv.hpp>
// #include <opencv2/videoio.hpp>
// #include <opencv2/highgui.hpp>
#include <base/Logger.hpp>

int capture()
{

  cv::VideoCapture cap("udpsrc port=5000 ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG,framerate=20/1 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink",
                       cv::CAP_GSTREAMER);
  if (!cap.isOpened())
  {
    std::cout << "Failed to open camera." << std::endl;
    return (-1);
  }

  cv::namedWindow("CSI Camera", cv::WINDOW_AUTOSIZE);
  cv::Mat img;

  std::cout << "Hit ESC to exit"
            << "\n";

  int rt = 0;
  while (true)
  {
    if (!cap.read(img))
    {
      std::cout << "Capture read error" << std::endl;
      break;
    }
    LOG_INFO;

    cv::imshow("CSI Camera", img);
    int keycode = cv::waitKey(1) & 0xff;
    if (keycode == 27)
      break;
    else if (keycode == 13)
    {
      rt = 1;
      break;
    }
  }

  cap.release();
  cv::destroyAllWindows();
  return rt;
}

int main()
{
  while (true)
  {
    if (capture() == 0)
      break;
  }

  return 0;
}