from django.urls import path

from . import controllers

urlpatterns = [ 
    path('frame-count', controllers.frame_count, name='frame_count'),
    path('frame-list', controllers.frame_list, name='frame_list'),
    path('frame-test', controllers.frame_test, name='frame_test'), 
]
