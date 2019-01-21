from utils.http import get_json_response, success, failed
from .models import Frame

# Create your views here.

def frame_list(request):
    frame_list = Frame.objects.all()
    return get_json_response(frame_list)


def frame_test(request):

    from .darknet import test
    test()

    # if request.POST:
    from django.utils import timezone
    frame = Frame(object_type="person", frame_date=timezone.now(), cam_id=999)
    frame.save()

    return success()
    
    # return failed()