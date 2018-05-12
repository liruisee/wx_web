from django.shortcuts import render, render_to_response, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
import hashlib
from django.db import connection
from functools import wraps


# Create your views here.
def try_except_decorate(func):
        def inner(request, *args, **kwargs):
            try:
                result = func(request, *args, **kwargs)
                if result is None:
                    return JsonResponse({'result': 'failed', 'message': '网络异常'}, safe=False)
            except Exception as e:
                return JsonResponse({'result': 'failed', 'message': '网络异常'}, safe=False)
        return inner


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


def teacher_list(request):
    return render(request, 'teacher_list.html', {})


def teacher_info(request):
    return render(request, 'teacher_info.html', {})


def type_list(request):
    return render(request, 'type_list.html', {})


# 返回老是的type_list，用于ajax请求，类型{type1:[row1, row2, row3],type2:[row1, row2, row3]}
@try_except_decorate
def get_type_list(request):
    cursor = connection.cursor()
    try:
        sql = "select teacher_id,teacher_name,teacher_record,teacher_type,img_url,video_url,teacher_type_code from teachers"
        result_dic = {}
        row_key_list = ['teacher_id', 'teacher_name', 'teacher_record', 'teacher_type', 'img_url', 'video_url']
        cursor.execute(sql)
        for row in cursor.fetchall():
            teacher_type = str(row[-1])
            if teacher_type not in result_dic:
                result_dic[teacher_type] = [dict(zip(row_key_list, list(row[:-1])))]
            else:
                if len(result_dic[teacher_type]) < 3:
                    result_dic[teacher_type].append(dict(zip(row_key_list, list(row[:-1]))))
                else:
                    pass
        type_list = sorted(result_dic.keys())
        result_dic['type_list'] = type_list
        return JsonResponse(result_dic, safe=False)
    except Exception as e:
        print(e)
    finally:
        cursor.close()


def get_teacher_list_by_type(request):
    if request.method != 'GET':
        return HttpResponse("请求类型错误，请使用get请求")
    cursor = connection.cursor()
    try:
        teacher_type_code = request.GET['teacher_type_code']
        sql = "select teacher_id,teacher_name,teacher_record,teacher_type,img_url,video_url from teachers \
            where teacher_type_code='%s'" % teacher_type_code
        cursor.execute(sql)
        result = cursor.fetchall()
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(e)
    finally:
        cursor.close()



