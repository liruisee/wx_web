from django.urls import path
from wx_app import views, wx_server

urlpatterns = [
    path('', views.start),
    path('login/', views.login),
    path('index/', views.index),
    path('regist/', views.regist),
    path('check_signature/', wx_server.check_signature),
]
