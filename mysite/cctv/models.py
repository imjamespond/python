from django.db import models

# Create your models here.

class Frame(models.Model):
    object_type = models.CharField(max_length=200)
    frame_date = models.DateTimeField('frame date')
    cam_id = models.IntegerField(default=0)

class Cam(models.Model):
    name = models.CharField(max_length=200)
    ip_addr = models.CharField('ip address of cam', max_length=200)

