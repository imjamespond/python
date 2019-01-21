from django.urls import path

from . import controllers

urlpatterns = [ 
    path('frame-list', controllers.frame_list, name='frame_list'),
    path('frame-test', controllers.frame_test, name='frame_test'),
]
