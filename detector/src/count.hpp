#include "detect.hpp"

template <typename TrackerType>
void count(TrackerType &tracker, float left, float top, float right, float bottom, int *count)
{
    if (tracker.disabled)
        return;


    tracker.distY += tracker.last.y - tracker.roi.y;
    tracker.distX += tracker.last.x - tracker.roi.x;

    if (tracker.roi.y < top && (tracker.last.y > top || tracker.distY > 20.0f) ) 
    {
        count[0]++;
        tracker.disabled = true;
    }
    if ((tracker.roi.y + tracker.roi.height) > bottom && (((tracker.last.y + tracker.last.height) < bottom) || tracker.distY < -20.0f)) 
    {
        count[1]++;
        tracker.disabled = true;
    }
    if (tracker.roi.x < left && /*tracker.last.x > left &&*/ tracker.distX > 20.0f)
    {
        count[2]++;
        tracker.disabled = true;
    }
    if ((tracker.roi.x + tracker.roi.width) > right && tracker.distX > -20.0f /*(tracker.last.x + tracker.last.width) < right &&*/)
    {
        count[3]++;
        tracker.disabled = true;
    }
}