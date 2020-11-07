import PIL
from django.http import JsonResponse
from trytest.models import User, Dishes, Trade, TradeDish, ProposalUserLike, ProposalImage, Proposal
from ..tools import *
import time, random
import trytest.tools
import json
import re


def new_proposal(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    data_get = request.POST
    images = request.FILES.getlist('images')

    introduction = data_get.get('introduction')
    pname = data_get.get('pname')
    the_proposal = Proposal(Introduction=introduction, PName=pname, User_id=int(user_id), Support=0, PStatus="打开")
    try:
        the_proposal.save()
    except:
        return JsonResponse({"etst": "tesssssst"})
    for image in images:
        image_obj = ProposalImage(Proposal_id=the_proposal.id, Picture=image)
        try:
            image_obj.save()
        except Exception as e:
            return JsonResponse({"Status": -1, "msg": e.__str__(),
                                 "t": image_obj.__str__(), "a": image.__str__()})
    return JsonResponse({"Status": 1, "msg": "发表提案成功", "name": image_road(ProposalImage.objects.filter(Proposal_id=the_proposal.id)[0].Picture.__str__())})


def likes_change(request):
    if not request.session.get('is_login', False):
        return JsonResponse({"status": -2, "msg": "please sign in first"})
    user_id = request.session["user_id"]

    if request.method == "POST":
        data_get = json.loads(request.body)
    elif request.method == "GET":
        data_get = request.GET
    else:
        return JsonResponse({"success": 0, "msg": "request error"})
    proposal_id = data_get.get("proposal_id")
    data = user_id.__str__()+"|"+proposal_id.__str__()
    if ProposalUserLike.objects.filter(Data__exact=data).delete():
        tmp = Proposal.objects.get(id=proposal_id)
        tmp.Support -= 1
    else:
        ProposalUserLike(Data=data).save()
        tmp = Proposal.objects.get(id=proposal_id)
        tmp.Support += 1
    tmp.save()
    JsonResponse({"status": 1, "msg": "change succeed"})

