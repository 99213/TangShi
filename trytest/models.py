from django.db import models
import datetime
from django.utils import timezone


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


class User(models.Model):
    UserName = models.CharField(max_length=10, null=True)
    Password = models.CharField(max_length=20)
    PhoneNumber = models.IntegerField()
    StudentNumber = models.IntegerField()
    Money = models.IntegerField(default=0)


class Proposal(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Picture = models.ImageField(null=True)
    Introduction = models.CharField(max_length=200)
    PName = models.CharField(max_length=20)
    Support = models.IntegerField(null=True)
    PStatus = models.BooleanField()
# Create your models here.


class Dishes(models.Model):
    DishName = models.CharField(max_length=10)
    DishBrief = models.CharField(max_length=200, null=True)
    DishPic = models.ImageField(null=True)
    DishScore = models.IntegerField(null=True)
    DishPrice = models.FloatField(max_length=5)
    DishSell = models.IntegerField(default=0, null=True)


class Trade(models.Model):
    Canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Code = models.CharField(max_length=50)
    TStatus = models.BooleanField()
    OrderTime = models.TimeField(auto_now_add=True)
    CloseTime = models.TimeField(null=True)
    Cost = models.FloatField(max_length=5)


class TradeComment(models.Model):
    Trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    Content = models.CharField(max_length=200)
    Reply = models.CharField(max_length=200, null=True)


class TradeDish(models.Model):
    Dishes = models.ForeignKey(Dishes, on_delete=models.CASCADE, null=True)
    Trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True)
    CommentScore = models.IntegerField(null=True)