#include "detect.hpp"

void countTest(DarknetTracker& tracker, float left,float top,float right,float bottom, int* count)
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
    if (tracker.last.x > left && tracker.roi.x < left) 
    {
        count[2]++;
        tracker.disabled = true;
    }
    if (tracker.last.x < right && tracker.roi.x > right) 
    {
        count[3]++;
        tracker.disabled = true;
    }
}