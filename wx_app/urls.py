from django.urls import path
from wx_app import views, wx_server

urlpatterns = [
    path('', views.start),
    path('login/', views.login),
    path('regist/', views.regist),
    path('check_signature/', wx_server.check_signature),
    path('teacher_list/', views.teacher_list),
    path('teacher_info/', views.teacher_info),
    path('type_list/', views.type_list),
    path('get_type_list/', views.get_type_list),
]

