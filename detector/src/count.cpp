#include "detect.hpp"

void count(DarknetTracker& tracker, float left,float top,float right,float bottom, int* count)
{
    if (tracker.disabled)
        return;

    if (tracker.last.y > top && tracker.roi.y < top) 
    {
        count[0]++;
        tracker.disabled = true;
    }
    if (tracker.last.y < bottom && tracker.roi.y > bottom) 
    {
        count[1]++;
        tracker.disabled = true;
    }
    if ((tracker.last.x + tracker.last.width * .5) > left && (tracker.roi.x + tracker.roi.width * .5) < left) 
    {
        count[2]++;
        tracker.disabled = true;
    }
    if ((tracker.last.x + tracker.last.width * .5) < right && (tracker.roi.x + tracker.roi.width * .5) > right) 
    {
        count[3]++;
        tracker.disabled = true;
    }
}