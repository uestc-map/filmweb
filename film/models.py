import django.utils.timezone as timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse

class UserProfile(AbstractUser):
    money = models.IntegerField(max_length=20, default=0,blank=False, verbose_name='余额')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class order(models.Model):
    orderId = models.IntegerField(max_length=20, primary_key=True, blank=False,verbose_name='订单号')
    seat = models.CharField(max_length=10, blank=False,verbose_name="座位号")
    dateTime=models.ForeignKey('filmscence',on_delete=models.CASCADE,verbose_name="场次")
    userName = models.ForeignKey('UserProfile', on_delete=models.CASCADE,verbose_name="用户名",default="admin")
    filmName = models.ForeignKey('film', on_delete=models.CASCADE,verbose_name="电影名")
    order_m=models.IntegerField(max_length=20,default='0',verbose_name='实付金额')
    order_time=models.TimeField(auto_now_add=True,verbose_name='购票时间')
    class Meta:
        ordering=['userName','-dateTime','-order_time']
        verbose_name="订单"
        verbose_name_plural = verbose_name

class filmscence(models.Model):
    dateTime = models.DateTimeField(primary_key=True,default=timezone.now,verbose_name='时间')
    seat = models.CharField(max_length=300,default='0',verbose_name='已售座位列表')
    filmName = models.ForeignKey('film', on_delete=models.CASCADE,verbose_name='电影名')
    price= models.IntegerField(max_length=20,  blank=False,default=30,verbose_name='票价')
    remain=models.IntegerField(max_length=20,default='99',verbose_name='剩余座位')
    money=models.IntegerField(max_length=20,default='0',verbose_name='场次票房')
    class Meta:
        ordering=['-dateTime']
        verbose_name = "场次"
        verbose_name_plural = verbose_name

class daily(models.Model):
    date=models.DateField(primary_key=True,default='1999-01-01',verbose_name='日期')
    money = models.IntegerField(max_length=20, default='0', verbose_name='票房')
    class Meta:
        ordering=['-date']
        verbose_name = "每日票房"
        verbose_name_plural = verbose_name

class film(models.Model):
    filmName = models.CharField(max_length=20, primary_key=True, blank= False,verbose_name='电影名')
    filmDName = models.CharField(max_length=20, blank=False,verbose_name='导演')
    filmAName = models.CharField(max_length=45,blank=False,verbose_name='演员')
    filmScore = models.FloatField(default='0',verbose_name='评分')
    image = models.ImageField(upload_to="film/filmimage/",default='',verbose_name='海报')
    category = models.CharField(max_length=10, blank= False, default= '动作',verbose_name='分类')
    evaluateNum = models.IntegerField(max_length=10,default=0,verbose_name='评分人次')
    showDate = models.DateField(blank=False,default='1999-01-01',verbose_name='上映时间')
    deleteDate = models.DateField(blank=False,default='1999-01-01',verbose_name='下线时间')
    # filmSum = models.CharField(max_length=1000,default='0',verbose_name='总评分')
    filmScoreUser=models.CharField(max_length=1000,default='0',verbose_name='已评分用户id')#打过分的用户id
    total=models.IntegerField(max_length=20,default=0,verbose_name='票房')  #电影票房
    class Meta:
        ordering=['-filmScore','showDate']
        verbose_name = "电影"
        verbose_name_plural = verbose_name
