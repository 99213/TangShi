from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from trytest.models import User, Dishes, Trade, TradeDish
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

    username = data_get.get("username")
    phonenumber = data_get.get("phonenumber")
    studentnumber = data_get.get("studentnumber")
    password = data_get.get("password")

    this_user = User(UserName=username, Password=password, StudentNumber=studentnumber, PhoneNumber=phonenumber)
    try:
        User.objects.get(UserName=username)
        return JsonResponse({"status": -1, "msg": "user name exists"})
    except:
        try:
            User.objects.get(StudentNumber=studentnumber)
            return JsonResponse({"status": -1, "msg": "student has already register"})
        except:
            try:
                User.objects.get(PhoneNumber=phonenumber)
                return JsonResponse({"status": -1, "msg": "phone user has register"})
            except:
                ret = re.match(r"^1[35678]\d{9}$", phonenumber)
                if ret:
                    this_user.save()
                    return JsonResponse({"status": 1, "msg": "注册成功"})
                else:
                    return JsonResponse({"status": -1, "msg": "not a phone number"})


def cost(dish):
    costnum = 0
    for dish_id, dish_num in dish.items():
        dish_obj = Dishes.objects.get(pk=dish_id)
        costnum = dish_obj.DishPrice * dish_num + costnum
    return costnum


def transaction_receipt_generation():
    return random.randint(100000000, 999999999)


def order(request):
    data_get = request.POST
    dish = data_get.get("dish")
    costnum = cost(dish)
    user_id = data_get.get("user_id")
    canteen_id = data_get.get("canteen_id")
    trade_record = Trade(Code=transaction_receipt_generation(), Tstatus="待付款", Cost=costnum,
                         Canteen_id=canteen_id, User_id=user_id)
    trade_record.save()

    for _dish in dish:
        trade_dish_record = TradeDish(Dishes_id=_dish, Trade_id=trade_record.pk)
        trade_dish_record.save()

    return JsonResponse({"status": 1, "msg": "订单生成成功"})


def pay(request):
    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET

    trade_id = data_get.get("trade_id")
    JsonResponse({"status": 1, "Two-Dimensional Code": pay(trade_id.Cost)})


def pay_to_canteen(money):    # 返回固定收款额的食堂收款码
    return "now wait for this module done"


def get_order_status(request):
    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET
    trade_id = data_get.get("trade_id")
    handle_trade = Trade.objects.get(pk=trade_id)
    t_status = handle_trade.TStatus
    JsonResponse({"status": 1, "TStatus": t_status})


def canteen_get_money(request):
    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET
    trade_id = data_get.get("trade_id")
    handle_trade = Trade.objects.get(pk=trade_id)
    handle_trade.TStatus = "已付款"
    handle_trade.save()
    JsonResponse({"status": 1, "TStatus": "待付款->已付款"})