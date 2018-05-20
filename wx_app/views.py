from django.shortcuts import render, render_to_response, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
import hashlib
from django.db import connection
from functools import wraps
import traceback


# 异常处理，因为
def try_except_decorate(func):
        def inner(request, *args, **kwargs):
            try:
                result = func(request, *args, **kwargs)
                if result is None:
                    return JsonResponse({'result': 'failed', 'message': '网络异常'}, safe=False)
                else:
                    return result
            except Exception as e:
                return JsonResponse({'result': 'failed', 'message': str(e)}, safe=False)
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
        sql = "select id,name,introduce,se_class,img_url,video_url,fi_class from wx_teacher_info"
        result_dic = {}
        row_key_list = ['id', 'name', 'intorduce', 'se_class', 'img_url', 'video_url', 'fi_class']
        cursor.execute(sql)
        for row in cursor.fetchall():
            fi_class = str(row[-1])
            if fi_class not in result_dic:
                result_dic[fi_class] = [dict(zip(row_key_list, list(row)))]
            else:
                if len(result_dic[fi_class]) < 3:
                    result_dic[fi_class].append(dict(zip(row_key_list, list(row))))
                else:
                    pass
        type_list = sorted(result_dic.keys())
        result_dic['type_list'] = type_list
        return JsonResponse(result_dic, safe=False)
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@try_except_decorate
def get_teacher_list_by_type(request):
    if request.method != 'GET':
        return HttpResponse("请求类型错误，请使用get请求")
    cursor = connection.cursor()
    try:
        fi_class = request.GET['fi_class']
        row_key_list = ['id', 'name', 'intorduce', 'fi_class', 'img_url', 'video_url', 'se_class']
        sql = "select id,name,introduce,fi_class,img_url,video_url, se_class from wx_teacher_info \
            where fi_class='%s'" % fi_class
        cursor.execute(sql)
        result = [[dict(zip(row_key_list, list(row)))] for row in cursor.fetchall()]
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        cursor.close()


@try_except_decorate
def get_teacher_info(request):
    if request.method != 'GET':
        return HttpResponse("请求类型错误，请使用get请求")
    cursor = connection.cursor()
    try:
        teacher_id = request.GET['id']
        row_key_list = ['id', 'name', 'introduce', 'fi_class', 'se_class', 'img_url', 'video_url', 'se_class']
        sql = "select id,name,introduce,fi_class,se_class,img_url,video_url,se_class from wx_teacher_info \
            where id='%s'" % teacher_id
        print(sql)
        cursor.execute(sql)
        result = [[dict(zip(row_key_list, list(row)))] for row in cursor.fetchall()]
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        cursor.close()


@try_except_decorate
def get_work_list(request):
    if request.method != 'GET':
        return HttpResponse("请求类型错误，请使用get请求")
    cursor = connection.cursor()
    try:
        teacher_id = request.GET['id']
        sql = "select work from wx_teacher_work \
            where id='%s'" % teacher_id
        print(sql)
        cursor.execute(sql)
        result = {'work_list': [x for x in cursor.fetchall()]}
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        cursor.close()
