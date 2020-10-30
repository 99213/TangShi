from trytest.models import User, Dishes, Trade, TradeDish, DishesImage, ProposalImage
import random
from django.http import JsonResponse


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