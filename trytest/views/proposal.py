
from django.http import JsonResponse
from trytest.models import User, Dishes, Trade, TradeDish, DishesImage, ProposalImage, Proposal
from ..tools import *
import time, random

def new_proposal(request):
    data_get = request.POST
    images = request.FILES.getlist('images')
    introduction = data_get.get('introduction')
    pname = data_get.get('pname')
    user_id = data_get.get('user_id')
    the_proposal = Proposal(Introduction=introduction, PName=pname, User_id=int(user_id), Support=0, PStatus="打开")
    for image in images:
        image_obj = ProposalImage(Proposal_id=the_proposal.pk, Picture=image)
        image_obj.save()
    the_proposal.save()
    return JsonResponse({"Status": 1, "msg": "发表提案成功"})
