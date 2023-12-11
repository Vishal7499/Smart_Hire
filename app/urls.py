from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name= "home"),
    path("log_in", views.log_in, name= "log_in"),
    path("register", views.register, name= "register"),
    path("dashboard", views.dashboard, name= "dashboard"),
    path("cam_capture", views.cam_capture, name= "cam_capture"),
    path('video_feed', views.video_feed, name='video_feed'),
    path("feedback", views.feedback, name= "feedback"),
    path("result", views.result, name= "result"),
    path("log_out", views.log_out, name= "log_out"),
]
