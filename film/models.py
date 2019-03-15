
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class order(models.Model):
    orderId = models.IntegerField(max_length=20, primary_key=True, blank=False)
    filmName = models.CharField(max_length=20, blank=False)
    seat = models.IntegerField(max_length=2, blank=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    userId=models.ForeignKey('User', on_delete=models.CASCADE)


class filmscence(models.Model):
    dateTime=models.DateTimeField(primary_key=True)
    seat= models.IntegerField(max_length=300)
    filmName=models.ForeignKey('film', on_delete=models.CASCADE)


class film(models.Model):
    filmName=models.CharField(max_length=20, primary_key=True, blank= False)
    filmDName=models.CharField(max_length=20, blank=False)
    filmAName=models.CharField(max_length=45,blank=False)
    filmScore=models.FloatField(default=0)
    Route=models.CharField(max_length=20,blank= False)
    category =models.CharField(max_length=10, blank= False, default= '动作')
    evaluateNum=models.IntegerField(max_length=10,default=0)
    showDate=models.DateField(blank=False)
    deleteDate=models.DateField(blank=False)