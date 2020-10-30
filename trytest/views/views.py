# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from trytest.models import User, Dishes, Trade, TradeDish, DishesImage, ProposalImage
import random
import re

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
        return JsonResponse({"status": 1, "msg": "登录成功", "data": "true"})
    else:
        return JsonResponse({"status": 0, "msg": "登录失败"})


def register(request):
    if request.method == "POST":
        data_get = request.POST
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
        ret = re.match(r"^1[35678]\d{9}", phonenumber)
        if ret:
            try:
                this_user.save()
            except:
                if type(phonenumber) is str:
                    return JsonResponse({"status": -1, "msg": "错误2"})
                return JsonResponse({"status": -1, "msg": "错误1"+this_user.PhoneNumber})
            return JsonResponse({"status": 1, "msg": "register succeed"})
        else:
            return JsonResponse({"status": -1, "msg": "not a phone number"})

  # except:
 # return JsonResponse({"status": -1, "msg": "后端错误"})


