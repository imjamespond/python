from django.db import models
import json

# Create your models here.

class Frame(models.Model):
    frame_date = models.DateTimeField('frame date')
    cam_id = models.IntegerField(default=0)
    probability = models.FloatField(default=0)
    object_type = models.CharField(max_length=200)
    position = models.CharField(max_length=200, default='')

    idx_frame_date = models.Index(fields=['-frame_date'])

class Track(models.Model):
    track_date = models.DateTimeField('track date')
    cam_id = models.IntegerField(default=0)

    left = models.IntegerField(default=0)
    top = models.IntegerField(default=0)
    right = models.IntegerField(default=0)
    bottom = models.IntegerField(default=0)

    idx_track_date = models.Index(fields=['-track_date'])


class WebCam(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField('address of cam', max_length=200, default='')
    left = models.IntegerField(default=0)
    top = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    cam_width = models.IntegerField(default=0)
    cam_height = models.IntegerField(default=0)


