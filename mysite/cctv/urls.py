from django.urls import path

from . import controllers

urlpatterns = [ 
    path('frame-count', controllers.frame_count, name='frame_count'),
    path('frame-list', controllers.frame_list, name='frame_list'),
    path('frame-test', controllers.frame_test, name='frame_test'), 

    path('webcam-list', controllers.webcam_list, name='webcam-list'),
    path('webcam-add', controllers.webcam_add, name='webcam-add'),
    path('webcam-del', controllers.webcam_del, name='webcam-del'),

    path('csrf-token', controllers.get_csrf_token, name='csrf-token'),
]
