from django.shortcuts import render, render_to_response, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
import hashlib


# Create your views here.

def start(request):
    # 以下三种方法结果是一样的，reverse的args为login所需的参数
    # return HttpResponseRedirect('/myapp/login')
    # return redirect('/myapp/login')
    return redirect(reverse(login, args=[]))


def login(request):
    return render(request, 'login.html', {})


def regist(request):
    if request.method != 'POST':
        return JsonResponse({'result': 'faild', 'message': 'regist faild'}, safe=False)
    try:
        post_data = request.POST
        user = post_data['user']
        email = post_data['email']
        password = post_data['password']
        user = User.objects.create_user(user, email, password)
        user.save()
        return JsonResponse({'result': 'success', 'message': 'regist success'}, safe=False)
    except Exception:
        return JsonResponse({'result': 'faild', 'message': 'regist faild'}, safe=False)


def get_access_token():
    pass


def teacher_list(request):
    return render(request, 'teacher_list.html', {})


def teacher_info(request):
    return render(request, 'teacher_info.html', {})


def type_list(request):
    return render(request, 'type_list.html', {})
