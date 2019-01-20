
from django.core import serializers
from django.http import HttpResponse

def get_json_response(data):
    json = serializers.serialize('json', data)

    return HttpResponse(json, content_type='application/json')

def success():
    return HttpResponse('success')

def failed(failed='failed :(', status=500):
    return HttpResponse(failed, status=status)