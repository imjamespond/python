from utils.http import queryset_to_json_response, json_response, success, failed, response
from .models import Frame, WebCam

from django.db import transaction, models
from django.middleware.csrf import get_token
import json


def get_csrf_token(request):
    return response(get_token(request))

def webcam_list(request):
    print(request.session)
    list = WebCam.objects.all()
    return queryset_to_json_response(list)

def webcam_add(request):
    
    model = WebCam(name=request.POST.get('name'),
                   address=request.POST.get('addr'))
    model.save()
    return success()

def webcam_del(request):
    list = WebCam.objects.filter(id=request.GET.get('id')).delete()
    return queryset_to_json_response(list)

def frame_list(request):
    # frame_list = Frame.objects.all()
    frame_list = Frame.objects.order_by('-pk')[0:10]
    return queryset_to_json_response(frame_list)


def frame_count(request):
    # rs = Frame.objects\
    #     .values('object_type','frame_date')\
    #     .annotate(count=models.Count('object_type'))
    rs = Frame.objects.raw(
        'select 1 as id, tmp.frame_date, tmp.object_type, count(tmp.object_type) as count from (SELECT * FROM cctv_frame ORDER BY ID DESC LIMIT 0, 8) as tmp group by tmp.frame_date, tmp.object_type order by tmp.frame_date desc')
    _rs = []
    for row in rs:
        _rs.append({'count': row.count, 'object_type': row.object_type, 'frame_date': str(row.frame_date)})
    return json_response(_rs)


def frame_del(request): 
    return success()


@transaction.atomic
def frame_test(request):

    from .darknet import test
    results = test()

    # if request.POST:
    from django.utils import timezone
    frame_date = timezone.now()
    for rs in results:
        frame = Frame(frame_date=frame_date, cam_id=999)
        frame.object_type = rs[0].decode('utf-8')
        frame.probability = rs[1]
        frame.position = json.dumps(rs[2])
        frame.save()

    return success()

    # return failed()
