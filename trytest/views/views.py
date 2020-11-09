# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from trytest.models import User, Dishes, FavoriteDish
import trytest.tools
import random
import re
import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def sign(request):
    if request.method == "POST":
        data_get = request.POST
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "sign failed"})

    phonenumber = data_get.get("phonenumber")
    studentnumber = data_get.get("studentnumber")
    password = data_get.get("password")
    try:
        this_user = User.objects.get(PhoneNumber=phonenumber)
    except:
        return JsonResponse({"status": -1, "msg": "user doesn't exist", "phonenumber": phonenumber})
    if this_user.Password == password:
        print("2233")
        request.session['is_login'] = True
        request.session['user_id'] = this_user.id
        return JsonResponse({"status": 1, "msg": "登录成功", "data": "true"})
    else:
        return JsonResponse({"status": 0, "msg": "登录失败"})


def register(request):
    if request.method == "POST":
        data_get = json.loads(request.body)
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "register failed"})

    username = random.randint(1, 999999999)

    phonenumber = data_get.get("phonenumber")

    studentnumber = data_get.get("studentnumber")
    password = data_get.get("password")

    this_user = User(UserName=username, Password=password, StudentNumber=studentnumber, PhoneNumber=phonenumber)

    """    
    try:
        User.objects.get(StudentNumber=studentnumber)
        return JsonResponse({"status": -1, "msg": "student has already register"})
    except:
    """
    try:
        User.objects.get(PhoneNumber=phonenumber)
        return JsonResponse({"status": -1, "msg": "phone user has register"})
    except:
        # try:
        """a=0
        if type(phonenumber) is str:
            a=1"""
        ret = re.match(r"^1[35678]\d{9}$", phonenumber)
        if ret:
            try:
                this_user.save()
            except:
                if type(phonenumber) is str:
                    return JsonResponse({"status": -1, "msg": "错误2"})
                return JsonResponse({"status": -1, "msg": "错误1" + this_user.PhoneNumber})
            return JsonResponse({"status": 1, "msg": "register succeed"})
        else:
            return JsonResponse({"status": -1, "msg": "not a phone number"})


def add_love_dish(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = json.loads(request.body)
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "request error"})

    dishes_id = int(data_get.get("dishes_id"))
    if FavoriteDish.objects.filter(User_id=user_id, Dishes_id=dishes_id):
        return JsonResponse({"status": 0, "msg": "菜品早已设置为收藏"})
    else:
        FavoriteDish(User_id=user_id, Dishes_id=dishes_id).save()
        return JsonResponse({"status": 1, "状态": "添加成功"})


def add_user_image(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = json.loads(request.body)
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "request error"})

    this_user = User.objects.get(id=user_id)
    for filename, file in request.FILES.iteritems():
        name = request.FILES[filename].name
        this_user.UserImage = file
        this_user.save()
    return JsonResponse({"status": 1, "msg": "头像上传成功"})


def get_tangshi_name(request):
    if request.method == "POST":
        data_get = json.POST
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "request error"})

    return JsonResponse({"status": 1, "mallName": "堂食"})
# except:
# return JsonResponse({"status": -1, "msg": "后端错误"})
