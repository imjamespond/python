from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('frame-list', views.frame_list, name='frame_list'),
    path('frame-test', views.frame_test, name='frame_test'),
]
