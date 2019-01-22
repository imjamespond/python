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

class Cam(models.Model):
    name = models.CharField(max_length=200)
    ip_addr = models.CharField('ip address of cam', max_length=200)

