import sched
import time
import json
import uuid
import os
import datetime
import threading

from urllib import request, parse
import urllib

from django.db.models.functions import TruncMinute
from django.db.models import Sum

from .models import Frame, WebCam, Track

hardware = json.loads(os.popen('lshw -quiet -json').read())
# print(hardware['serial'])

url = 'http://trueform-api-dev.azurewebsites.net/api/analysis'
scheduler = sched.scheduler(time.time, time.sleep)

# appfilename = os.path.join(os.path.dirname(__file__), 'appdata')
# appid = None

# try:
#     appfile = open(appfilename, "r")
#     appid = appfile.read(-1)
# except Exception as ex:
#     print(str(ex))
#     pass

# if appid:
#     print('app id:', appid)
# else:
#     appid = str(uuid.uuid1())
#     appfile = open(appfilename, "w")
#     appfile.write(appid)
# appfile.close()


def report(direction='Left', count=0, timestamp=int(round(time.time() * 1000))):
    obj = {}
    
    obj['StoreId'] = '22'
    obj['SourceId'] = hardware['serial']
    obj['Direction'] = direction
    obj['Count'] = '2'

    data = {}
    data['data'] = json.dumps(obj)
    data['timestamp'] = str(timestamp)
    data['type'] = '10'
    data['level'] = '1' 
    # print(json.dumps([data]))
    req = request.Request(url, data=parse.quote_plus(json.dumps([data])).encode())
    response = urllib.request.urlopen(req)

    print(timestamp, direction, count, response.read())

starttime = 0

def last_10_min():
    global starttime
    if(starttime == 0):
        starttime = datetime.datetime.now() - datetime.timedelta(seconds=60 * 10)
    track_list = Track.objects\
        .filter(track_date__range=(starttime, datetime.datetime.now()))\
        .annotate(minu=TruncMinute('track_date'))\
        .values('minu')\
        .annotate(sum_left=Sum('left'), sum_right=Sum('right'), sum_top=Sum('top'), sum_bottom=Sum('bottom'))
    
    starttime = datetime.datetime.now()
    
    for track in track_list:

        if(track['sum_left']>0):
          report(direction='Left',
                 count=track['sum_left'], 
                 timestamp=track['minu'].strftime("%s"))
        if(track['sum_right'] > 0):
          report(direction='Right',
                 count=track['sum_right'],
                 timestamp=track['minu'].strftime("%s"))
        if(track['sum_top'] > 0):
          report(direction='Top',
                 count=track['sum_top'],
                 timestamp=track['minu'].strftime("%s"))
        if(track['sum_bottom'] > 0):
          report(direction='Bottom',
                 count=track['sum_bottom'],
                 timestamp=track['minu'].strftime("%s"))

    scheduler.enter(3, 1, last_10_min)
    scheduler.run()

thread = threading.Thread(target=last_10_min, args=())
thread.start()
# thread.join()

# last_10_min()
# report()
