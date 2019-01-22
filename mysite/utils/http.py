
from django.core import serializers
from django.http import HttpResponse
import json


def json_response(data):
    _json = json.dumps(data)

    return HttpResponse(_json, content_type='application/json')


def queryset_to_json_response(data):
    _json = serializers.serialize('json', data)

    return HttpResponse(_json, content_type='application/json')


def success():
    return HttpResponse('success')


def failed(failed='failed :(', status=500):
    return HttpResponse(failed, status=status)
