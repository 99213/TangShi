from trytest.models import User, Dishes, Trade, TradeDish, TradeComment, DishesImage, Worker
import random
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader
import time
from tangshi.settings import *
from trytest.views.order import head_path
from trytest.views.order import name_search_dish_server, id_get_dish_dic
import json
import datetime


def worker_index(request):
    request.session.get('is_login_w', False)
    if request.session["is_login_w"]:
        worker_id = request.session["worker_id"]
        this_worker = Worker.objects.filter(id=worker_id)[0]

        return render(request, 'home.html', {'name': this_worker.WorkerName, 'position': this_worker.WorkerPosition,
                                             'phonenumber': this_worker.PhoneNumber,
                                             'photo': head_path + this_worker.Photo.name})
    return render(request, 'sign.html', {})


def worker_register(request):
    data_get = request.POST
    name = data_get.get('name')
    password = data_get.get("password")
    phonenumber = data_get.get("phonenumber")
    position = data_get.get('position')
    photo = request.FILES['photo']
    this_worker = Worker(WorkerName=name, WorkerPosition=position, PhoneNumber=phonenumber, Password=password)
    this_worker.save()
    this_worker1 = Worker.objects.get(PhoneNumber=phonenumber)
    this_worker1.Photo = photo
    this_worker1.save()

    return HttpResponse()


def worker_sign(request):
    data_get = request.POST
    password = data_get.get("password")
    phonenumber = int(data_get.get("phonenumber"))
    this_worker = Worker.objects.filter(PhoneNumber=phonenumber)
    if this_worker:
        this_worker = this_worker[0]
        if this_worker.Password == password:
            request.session['is_login_w'] = True
            request.session['worker_id'] = this_worker.id
            return JsonResponse({'code': '0'})
    else:
        return JsonResponse({'code': -1, 'err': '密码错误'})


def worker_home(request):
    if not request.session.get('is_login_w', False):
        return render(request, 'sign.html', {'err': '未登录'})
    worker_id = request.session["worker_id"]
    this_worker = Worker.objects.filter(id=worker_id)[0]

    return render(request, 'home.html', {'name': this_worker.WorkerName, 'position': this_worker.WorkerPosition,
                                         'phonenumber': this_worker.PhoneNumber,
                                         'photo': head_path + this_worker.Photo.name})


def dish_page(request):
    if not request.session.get('is_login_w', False):
        return render(request, 'sign.html', {'err': '未登录'})
    return render(request, 'dish.html', {})


def dish_modify(request):
    data_get = request.POST
    all_img_index = data_get.get('all_img_index')
    delete_index = all_img_index.split(',')
    if all_img_index == '':
        delete_index = []
    index_to_img_id = data_get.get('index_to_img_id')
    index_to_img_id = json.loads(index_to_img_id)
    new_price = data_get.get('new_price')
    new_brief = data_get.get('new_brief')
    new_category = data_get.get('new_category')
    new_name = data_get.get('new_name')
    old_name = data_get.get('old_name')
    id = data_get.get('id')
    may_dish = {}
    handle_dish = {}
    if id == '':
        may_dish = name_search_dish_server(old_name)
        if len(may_dish) == 0:
            return JsonResponse({'code': -1, 'message': '0 result'})
        elif len(may_dish) > 1:
            return JsonResponse({'code': -1, 'message': 'too many result', 'may_dishes': may_dish})
        else:
            for key in may_dish.keys():
                handle_dish = Dishes.objects.get(DishName=key)
    else:
        try:
            handle_dish = Dishes.objects.get(id=int(id))
        except:
            return JsonResponse({'code': -1, 'message': '0 result'})
    if not new_name == '':
        handle_dish.DishName = new_name
    if not new_brief == '':
        handle_dish.DishBrief = new_brief
    if not new_price == '':
        handle_dish.DishPrice = int(new_price)
    handle_dish.DishCategoryId_id = new_category

    for img_index in delete_index:
        try:
            DishesImage.objects.get(id=index_to_img_id[handle_dish.id.__str__()][img_index.__str__()]).delete()
        except:
            return JsonResponse({'code': -1, 'message': '无此图'})

    for img in request.FILES.getlist('new_imgs'):
        handle_img = DishesImage(DishPic=img, Dishes_id=handle_dish.id)
        try:
            handle_img.save()
        except Exception as e:
            a = 1
    handle_dish.save()
    return JsonResponse({'code': 0})


def new_dish(request):
    if not request.session.get('is_login_w', False):
        return render(request, 'sign.html', {'err': '未登录'})
    data_get = request.POST
    name = data_get.get('name')
    try:
        Dishes.objects.get(DishName=name)
        return JsonResponse({'code': -1, 'message': 'same name'})
    except:
        a = 1
    brief = data_get.get('brief')
    price = data_get.get('price')
    category = data_get.get('category')
    try:
        handle_dish = Dishes(DishName=name, DishBrief=brief, DishScore=10, DishPrice=price, DishSell=0,
                             DishCategoryId_id=category)
        for img in request.FILES.getlist('new_imgs'):
            handle_img = DishesImage(DishPic=img, Dishes_id=handle_dish.id)
            try:
                handle_img.save()
            except Exception as e:
                print(e)
        handle_dish.save()
        return JsonResponse({'code': 0, 'message': '新增菜品成功'})
    except Exception as e:
        print(e)
        return JsonResponse({'code': -1, 'message': '新增菜品失败'})


def delete_dish(request):
    if not request.session.get('is_login_w', False):
        return render(request, 'sign.html', {'err': '未登录'})
    data_get = request.POST
    dish_id = data_get.get('dish_id')
    if dish_id == "":
        name = data_get.get('dish_name')
        if name is None:
            name = ""
        name_id = name_search_dish_server(name)
        names = name_id.keys()

        if len(names) > 1:
            return JsonResponse({'code': -1, 'message': 'too many result', 'may_dishes': name_id})
        elif len(names) == 0:
            return JsonResponse({'code': -1, 'message': '0 result'})
        else:
            for key in names:
                dish_id = name_id[key]['dish_id']
            Dishes.objects.get(id=dish_id).delete()
            return JsonResponse({'code': 0, 'message': '成功删除' + names[0]})
    else:
        try:
            handle_dish = Dishes.objects.get(id=dish_id)
            name = handle_dish.DishName
            handle_dish.delete()
            return JsonResponse({'code': 0, 'message': '成功删除' + name})
        except:
            return JsonResponse({'code': -1, 'message': 'id错误'})


def comment_reply(request):
    dishes = Dishes.objects.filter()
    dishes_id = {}
    for dish in dishes:
        dishes_id[dish.id] = dish.DishName

    recent_trades = Trade.objects.filter(CloseTime__gt=(datetime.datetime.now() - datetime.timedelta(days=7)),
                                         TStatus='已完成')
    trades_id = {}
    tradesDish = []
    dish_comment = {}
    dishid_tradedishid = {}
    tradedishid_commentid_commentcontent = {}
    for trade in recent_trades:
        trades_id[trade.id] = trade.User_id
        tradedishList = TradeDish.objects.filter(Trade_id=trade.id)
        for each_dish in tradedishList:
            tradesDish.append({'id': each_dish.id, 'CommentScore': each_dish.CommentScore,
                               'Dishes_id': each_dish.Dishes_id, 'Trade_id': each_dish.Trade_id})
    for each_s_dish in tradesDish:
        all_comments = TradeComment.objects.filter(TradeDish_id=each_s_dish['id'])
        if not dishid_tradedishid.__contains__(each_s_dish['Dishes_id']):
            dishid_tradedishid[each_s_dish['Dishes_id']] = []
        dishid_tradedishid[each_s_dish['Dishes_id']].append(each_s_dish['id'])
        tradedishid_commentid_commentcontent[each_s_dish['id']] = {}
        for each_Comment in all_comments:
            tradedishid_commentid_commentcontent[each_s_dish['id']][each_Comment.id] = \
                {'Content': each_Comment.Content, 'TradeDish_id': each_Comment.TradeDish_id,
                 'ReplyId': each_Comment.ReplyId, 'WorkerId_id': each_Comment.WorkerId_id}
    return render(request, "eater.html", {"dishid_tradedishid": dishid_tradedishid, "dishes_id": dishes_id,
                                          "tradedishid_commentid_commentcontent": tradedishid_commentid_commentcontent})


def get_comment(request):
    dishes = Dishes.objects.filter()
    dishes_id = {}
    for dish in dishes:
        dishes_id[dish.id] = dish.DishName

    recent_trades = Trade.objects.filter(CloseTime__gt=(datetime.datetime.now() - datetime.timedelta(days=7)),
                                         TStatus='已完成')
    trades_id = {}
    tradesDish = []
    dish_comment = {}
    dishid_tradedishid = {}
    tradedishid_commentid_commentcontent = {}
    for trade in recent_trades:
        trades_id[trade.id] = trade.User_id
        tradedishList = TradeDish.objects.filter(Trade_id=trade.id)
        for each_dish in tradedishList:
            tradesDish.append({'id': each_dish.id, 'CommentScore': each_dish.CommentScore,
                               'Dishes_id': each_dish.Dishes_id, 'Trade_id': each_dish.Trade_id})
    for each_s_dish in tradesDish:
        all_comments = TradeComment.objects.filter(TradeDish_id=each_s_dish['id'])
        if not dishid_tradedishid.__contains__(each_s_dish['Dishes_id']):
            dishid_tradedishid[each_s_dish['Dishes_id']] = []
        dishid_tradedishid[each_s_dish['Dishes_id']].append(each_s_dish['id'])
        tradedishid_commentid_commentcontent[each_s_dish['id']] = {}
        for each_Comment in all_comments:
            tradedishid_commentid_commentcontent[each_s_dish['id']][each_Comment.id] = \
                {'Content': each_Comment.Content, 'TradeDish_id': each_Comment.TradeDish_id,
                 'ReplyId': each_Comment.ReplyId, 'WorkerId_id': each_Comment.WorkerId_id,
                 "ReplyTime": each_Comment.ReplyTime, 'DishScore': each_s_dish['CommentScore']}
    for tdish_id,comments in tradedishid_commentid_commentcontent.items():
        for cid,cconcent in comments.items():
            temp = cconcent['ReplyId']
            i = '&nbsp&nbsp'
            if cconcent['WorkerId_id'] is not None:
                tradedishid_commentid_commentcontent[tdish_id][cid]['WorkerPosition'] = Worker.objects.get(id=each_Comment.WorkerId_id).WorkerPosition
                tradedishid_commentid_commentcontent[tdish_id][cid]['WorkerName'] = Worker.objects.get(id=each_Comment.WorkerId_id).WorkerName
                tradedishid_commentid_commentcontent[tdish_id][cid]["UserName"] = None
            else:
                tradedishid_commentid_commentcontent[tdish_id][cid]['WorkerPosition'] = None
                tradedishid_commentid_commentcontent[tdish_id][cid]['WorkerName'] = None
                tdid = tradedishid_commentid_commentcontent[tdish_id][cid]['TradeDish_id']
                tid = TradeDish.objects.get(id=tdid).Trade_id
                uid = Trade.objects.get(id=tid).User_id
                uname = User.objects.get(id=uid).UserName
                tradedishid_commentid_commentcontent[tdish_id][cid]["UserName"] = uname
            while comments.__contains__(temp):
                i += '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'
                temp = comments[temp]['ReplyId']
            tradedishid_commentid_commentcontent[tdish_id][cid]['level'] = i
    return JsonResponse({"dishid_tradedishid": dishid_tradedishid, "dishes_id": dishes_id,
                         "tradedishid_commentid_commentcontent": tradedishid_commentid_commentcontent})
