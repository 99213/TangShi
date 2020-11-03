from django.db import models
import time
import random
from django.utils import timezone
import datetime
from django.shortcuts import render
from tangshi.settings import *


class Question(models.Model):

    def __str__(self):
        return self.question_text

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):

    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Canteen(models.Model):
    Cname = models.CharField(max_length=20)


class Dishes(models.Model):
    DishName = models.CharField(max_length=10)
    DishBrief = models.CharField(max_length=200, null=True)
    DishScore = models.IntegerField(null=True)
    DishPrice = models.FloatField(max_length=5)
    DishSell = models.IntegerField(default=0, null=True)


class DishesImage(models.Model):
    Dishes = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    DishPic = models.ImageField(null=True, upload_to='picture',)


def load_user_image(instance, filename):
    return '/'.join([MEDIA_ROOT, "user_image", instance.id, time.strftime('%Y%m%d%H%M%S')
                     + random.randint(1000000, 9999999).__str__()])


class User(models.Model):
    UserImage = models.ImageField(null=True, upload_to=load_user_image)
    UserName = models.CharField(max_length=10, default=0)
    Password = models.CharField(max_length=20)
    PhoneNumber = models.FloatField(max_length=20)
    StudentNumber = models.IntegerField(null=True)
    Money = models.IntegerField(default=0, null=True)


class FavoriteDish(models.Model):
    Dishes = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)


class Proposal(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Introduction = models.CharField(max_length=200)
    PName = models.CharField(max_length=20)
    Support = models.IntegerField(null=True)
    PStatus = models.BooleanField()


def load_proposal_image(instance, filename):
    return '/'.join([MEDIA_ROOT, "proposal_images", instance.Proposal_id, time.strftime('%Y%m%d%H%M%S')
                     + random.randint(1000000, 9999999).__str__()])


class ProposalImage(models.Model):
    Proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    Picture = models.ImageField(null=True, upload_to=load_proposal_image, blank=True)


class ProposalUserLike(models.Model):
    Data = models.CharField(max_length=40, primary_key=True)


class Trade(models.Model):
    Canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Code = models.CharField(max_length=50)
    TStatus = models.BooleanField()
    OrderTime = models.TimeField(auto_now_add=True)
    CloseTime = models.TimeField(null=True,)
    Cost = models.FloatField(max_length=5)


class TradeComment(models.Model):
    Trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    Content = models.CharField(max_length=200)
    Reply = models.CharField(max_length=200, null=True)


class TradeDish(models.Model):
    Dishes = models.ForeignKey(Dishes, on_delete=models.CASCADE, null=True)
    Trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True)
    CommentScore = models.IntegerField(null=True)

