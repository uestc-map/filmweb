
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
import django.utils.timezone as timezone

class order(models.Model):
    orderId = models.IntegerField(max_length=20, primary_key=True, blank=False)
    filmName = models.CharField(max_length=20, blank=False)
    seat = models.CharField(max_length=2, blank=False)
    dateTime = models.DateTimeField(blank=False, default=timezone.now)
    userId = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    class Meta:
        ordering=['userId','-dateTime']

class filmscence(models.Model):
    dateTime = models.DateTimeField(primary_key=True, default=timezone.now)
    seat = models.CharField(max_length=300,default ='0')
    filmName = models.ForeignKey('film', on_delete=models.CASCADE)
    class Meta:
        ordering=['dateTime']


class film(models.Model):
    filmName = models.CharField(max_length=20, primary_key=True, blank= False)
    filmDName = models.CharField(max_length=20, blank=False)
    filmAName = models.CharField(max_length=45, blank=False)
    filmScore = models.FloatField(default=0)
    image = models.ImageField(upload_to="film/filmimage/",default='')
    category = models.CharField(max_length=10, blank= False, default= '动作')
    evaluateNum = models.IntegerField(max_length=10,default=0)
    showDate = models.DateField(blank=False, default='1999-01-01')
    deleteDate = models.DateField(blank=False, default='1999-01-01')
    filmSum = models.CharField(max_length=1000, default=' ')
    filmScoreUser=models.CharField(max_length=1000,default=' ')#打过分的用户id
    class Meta:
        ordering=['-filmScore','showDate']
