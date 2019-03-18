from .models import Track
from django.utils import timezone

def onTrack(t,b,l,r, cam_id):
    track = Track(
        track_date=timezone.now(),
        cam_id=cam_id,
        left=l,
        right=r,
        top=t,
        bottom=b)

    if (l>0 or r>0 or t>0 or b>0):
        track.save()