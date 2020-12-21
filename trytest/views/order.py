from trytest.models import User, Dishes, Trade, TradeDish, TradeComment, DishesImage, Category
import random
from django.http import JsonResponse
import time
from tangshi.settings import *
import json
import trytest.tools
from django.utils import timezone


head_path = 'http://127.0.0.1:8000' + MEDIA_URL


def cost(dishes_id_num):
    costnum = 0
    for dish_id, dish_num in dishes_id_num.items():
        dish_obj = Dishes.objects.get(pk=dish_id)
        costnum = dish_obj.DishPrice * dish_num + costnum
    return costnum


def transaction_receipt_generation():
    return random.randint(100000000, 999999999)


def order(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    data_get = json.loads(request.body)
    dishes_id_num = data_get["dishes_id_num"]
    costnum = cost(dishes_id_num)
    canteen_id = int(data_get["canteen_id"])
    trade_record = Trade(Code=transaction_receipt_generation(), TStatus="待付款", Cost=costnum,
                         Canteen_id=canteen_id, User_id=user_id)
    trade_record.save()

    for dish_id in dishes_id_num:
        trade_dish_record = TradeDish(Dishes_id=dish_id, Trade_id=trade_record.pk)
        trade_dish_record.save()

    return JsonResponse({"status": 1, "msg": "订单生成成功"})


def pay(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET

    trade_id = int(data_get.get("trade_id"))
    this_trade = Trade.objects.get(id=trade_id)
    if not user_id == this_trade.User_id:
        return JsonResponse({"status": 0, "msg": "not your trade"})
    return JsonResponse({"status": 1, "Two-Dimensional Code": pay_to_canteen(this_trade.Cost)})


def pay_to_canteen(money):  # 返回固定收款额的食堂收款码
    return "now wait for this module done"


def get_order_status(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET
    trade_id = int(data_get.get("trade_id"))
    handle_trade = Trade.objects.get(pk=trade_id)

    if not user_id == handle_trade.User_id:
        return JsonResponse({"status": 0, "msg": "not your order"})

    t_status = handle_trade.TStatus
    return JsonResponse({"status": 1, "TStatus": t_status})


def canteen_get_money(request):
    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET
    trade_id = int(data_get.get("trade_id"))
    handle_trade = Trade.objects.get(pk=trade_id)
    handle_trade.TStatus = "已付款"
    handle_trade.save()
    return JsonResponse({"status": 1, "TStatus": "待付款->已付款"})


def trade_comment(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET
    trade_id = int(data_get.get("trade_id"))
    this_trade = Trade.objects.get(id=trade_id)

    if not user_id == this_trade.User_id:
        return JsonResponse({"status": 0, "msg": "not your order"})

    if this_trade.TStatus == "待点评" or this_trade.TStatus == "已完成":
        comment = data_get.get("content")
        this_trade_comment = TradeComment(Content=comment, Trade_id=trade_id)
        this_trade_comment.save()
        return JsonResponse({"status": 1, "msg": "点评成功"})
    else:
        return JsonResponse({"status": 0, "msg": "当前订单不在可点评状态"})


def undo_order(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = request.POST
    else:
        data_get = request.GET
    trade_id = int(data_get.get("trade_id"))
    this_trade = Trade.objects.get(id=trade_id)

    if not user_id == this_trade.User_id:
        return JsonResponse({"status": 0, "msg": "not your order"})

    TStatus = this_trade.TStatus
    if TStatus == "待点评" or TStatus == "已完成":
        return JsonResponse({"status": 0, "msg": "订单已完成，不可撤销"})
    elif TStatus == "已付款":
        refund(trade_id)
    this_trade.TStatus = "已取消"
    this_trade.CloseTime = timezone.now()
    this_trade.save()
    return JsonResponse({"status": 1, "msg": "取消成功，若您已付款，退款将很快返回您的付款账户"})


def refund(trade_id):
    test = "test"


def name_search_dish_server(dish_name):
    may_dishes = Dishes.objects.filter(DishName__contains=dish_name)
    dishes_dic = {}
    for dish in may_dishes:
        dishes_dic[dish.DishName] = id_get_dish_dic(dish.id)
    return dishes_dic


def name_search_dish(request):
    if request.method == "POST":
        data_get = request.POST
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "request type error"})
    dish_name = data_get.get("dish_name")
    may_dishes = Dishes.objects.filter(DishName__contains=dish_name)
    dishes_dic = {}
    for dish in may_dishes:
        dishes_dic[dish.id] = id_get_dish_dic(dish.id)
    return JsonResponse({"status": 1, "content": dishes_dic})


def id_search_dish(request):
    if request.method == "POST":
        data_get = request.POST
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "request type error"})
    dish_dic = id_get_dish_dic(int(data_get.get("dish_id")))
    return JsonResponse({"status": 1, "content": dish_dic})


def get_all_dish(request):
    dishes_list = []
    dishes_obj = Dishes.objects.filter()
    for dish_obj in dishes_obj:
        dish_dic = id_get_dish_dic(dish_obj.id)
        dishes_list.append(dish_dic)
    return JsonResponse({"code": 0, "data": dishes_list})


def get_all_dish_detail(request):
    dishes_list = []
    dishes_obj = Dishes.objects.filter()
    for dish_obj in dishes_obj:
        dish_dic = id_get_dish_dic(dish_obj.id)
        dishes_list.append(dish_dic)
    return JsonResponse({"code": 0, "data": dishes_list})


def id_get_dish_dic(dish_id):
    dish = Dishes.objects.get(id=dish_id)
    dish_img_list = []
    dish_img_id_list = []
    img_list = DishesImage.objects.filter(Dishes_id=dish_id)
    for img in img_list:
        dish_img_list.append(head_path + img.DishPic.name)
        dish_img_id_list.append(img.id)
    if len(dish_img_list) > 0:
        dish_dic = {"dish_id": dish_id, "dish_name": dish.DishName, "dish_brief": dish.DishBrief,
                "dish_score": dish.DishScore, "dish_price": dish.DishPrice, "dish_sell": dish.DishSell,
                "img_list": dish_img_list, "img_id_list": dish_img_id_list, "afterSale": "0,1,2", "categoryId": dish.DishCategoryId_id,
                "commission": 0.00, "commissionType": 0, "dateAdd": "2020-11-09 23:59:14",
                "dateUpdate": "2020-11-24 09:24:28", "fxType": 2, "gotScore": dish.DishScore,
                "gotScoreType": 0, "hasAddition": False, "hidden": 0, "id": dish.id,
                "kanjia": False, "kanjiaPrice": 0.00, "limitation": False, "logisticsId": 0,
                "maxCoupons": 0, "miaosha": False, "minBuyNumber": 1, "minPrice": 20.00, "minScore": 0, "name": dish.DishName,
                "numberFav": 0, "numberGoodReputation": 0, "numberOrders": 0, "numberSells": dish.DishSell, "originalPrice": dish.DishPrice,
                "overseas": False, "paixu": 0,
                "pic": dish_img_list[0], "pingtuan": False,
                "pingtuanPrice": 0.00, "recommendStatus": 0, "recommendStatusStr": "普通", "sellEnd": False,
                "sellStart": True, "shopId": 0, "status": 0, "statusStr": "上架", "storeAlert": False, "stores": 895,
                "stores0Unsale": False, "type": 0, "unit": "份", "userId": 30600, "vetStatus": 1, "views": 2,
                "weight": 0.00}
    else:
        dish_dic = {"dish_id": dish_id, "dish_name": dish.DishName, "dish_brief": dish.DishBrief,
                "dish_score": dish.DishScore, "dish_price": dish.DishPrice, "dish_sell": dish.DishSell,
                "img_list": dish_img_list, "img_id_list": dish_img_id_list, "afterSale": "0,1,2", "categoryId": dish.DishCategoryId_id,
                "commission": 0.00, "commissionType": 0, "dateAdd": "2020-11-09 23:59:14",
                "dateUpdate": "2020-11-24 09:24:28", "fxType": 2, "gotScore": dish.DishScore,
                "gotScoreType": 0, "hasAddition": False, "hidden": 0, "id": dish.id,
                "kanjia": False, "kanjiaPrice": 0.00, "limitation": False, "logisticsId": 0,
                "maxCoupons": 0, "miaosha": False, "minBuyNumber": 1, "minPrice": 20.00, "minScore": 0, "name": dish.DishName,
                "numberFav": 0, "numberGoodReputation": 0, "numberOrders": 0, "numberSells": dish.DishSell, "originalPrice": dish.DishPrice,
                "overseas": False, "paixu": 0,
                "pic": head_path + 'proposal_images/9/202011032149129798005', "pingtuan": False,
                "pingtuanPrice": 0.00, "recommendStatus": 0, "recommendStatusStr": "普通", "sellEnd": False,
                "sellStart": True, "shopId": 0, "status": 0, "statusStr": "上架", "storeAlert": False, "stores": 895,
                "stores0Unsale": False, "type": 0, "unit": "份", "userId": 30600, "vetStatus": 1, "views": 2,
                "weight": 0.00}
    return dish_dic


def get_category(request):
    category = Category.objects.filter()
    all_category = []
    for eachcate in category:
        all_category.append(
            {'dateAdd': "2020-11-09 15:23:51", 'isUse': True, 'key': 1, 'level': 1, "paixu": 0, "pid": 0,
             "shopId": 0, "userId": 30600, 'id': eachcate.id, 'name': eachcate.Cname})
    return JsonResponse({'code': 0, 'data': all_category})


def add_dish(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    data_get = request.POST
    images = request.FILES.getlist('images')
