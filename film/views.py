from __future__ import unicode_literals
from .models import  order, film, filmscence
from django.shortcuts import render
import random
import re
from django.utils import timezone
import datetime
from django.views.generic import ListView
from django.views import generic
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.db import models

def register_User(request):
    if request.method== "POST":
        user_insert=User()
        user_insert.email= request.POST.get("userId",None)
        user_insert.username=request.POST.get("userName",None)
        user_insert.password=request.POST.get("password",None)
        if not all([ user_insert.email,user_insert.username,user_insert.password]):
            return render(request, 'film/register.html')
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', user_insert.email):
            return render(request, 'film/register.html', {'errmsg': '邮箱不符合规范'})

        try:
            user_Id=User.objects.get(email =user_insert.email)
            print(user_Id)

        except Exception as e:
            user_Id=None
        if user_Id:
            return render(request, 'film/register.html',{'errmsg':'邮箱已被使用'})

        pass_len=len(str(user_insert.password))
        if not (re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+',user_insert.password)) or (pass_len<6):
            return render(request, 'film/register.html',{'errmsg':'密码长度小于6位！'})
        user_insert.is_active =True
        user_insert.is_staff=False
        user_insert.is_superuser=False
        user_insert.save()
        return redirect('/film/login/')
    else:
        return render(request, 'film/register.html')


def login(request):
    if request.method == "POST":
        userId_login= request.POST.get("userId",None)
        password_login=request.POST.get("password",None)

        user_login = auth.authenticate(email=userId_login, password=password_login)
        if user_login is None:
            return render(request,"film/login.html",{"errmsg":"用户名或密码错误"})
        auth.login(request, user_login)
        return redirect("/film/home/")
    else:
        return render(request,'film/login.html')

def insert_order(request):
    if request.method== "POST":
        while True:
            orderId_test=random(0, 1000000000)
            try:
                orderId_exist=order.objects.get(orderId=orderId_test)
            except Exception as e:
                orderId_exist = None
            if not orderId_exist:
                break
        order_insert=order()
        order_insert.orderId=orderId_test
        order_insert.filmName=request.POST.get("filmName",None)
        order_insert.seat=request.POST.get("seat",None)
        order_insert.datetime=request.POST.get("datetime",None)
        order_insert.userId_id=user.objects.get(userId="userId")
        order_insert.save()
    return render(request, 'insert.html')


def insert_film(request):
    if request.method== "POST":
        film_insert=film()
        film_insert.filmName= request.POST.get("filmName",None)
        film_insert.filmDName=request.POST.get("filmDName",None)
        film_insert.image=request.POST.get("ROUTE",None)  #暂时还不会写
        film_insert.category=request.POSY.get("category",None)
        if not all([ film_insert.filmName, film_insert.filmDName, film_insert.Route, film_insert.category]):
            return render(request, 'insert.html')

        try:
           film_exist = film.objects.get(filmName=film_insert.filmName)
        except Exception as e:
            film_exist = None
        if film_exist:
            return render(request, 'insert.html', {'errmsg': '电影已存在'})
        return render(request, 'insert.html')

def insert_filmscence(request):
    if request.method== "POST":
        filmscence_insert=filmscence()
        filmscence_insert.datetime= request.POST.get("datetime",None)
        filmscence_insert.filmName_id=film.objects.get(filmName="filmName")
        try:
           datetime_exist = filmscence.objects.get(datetime=filmscence_insert.datetime)
        except Exception as e:
            datetime_exist = None
        if datetime_exist:
            return render(request, 'insert.html', {'errmsg': '该场次已有电影'})
        return render(request, 'insert.html')


def home_page(request): #主页
    now = datetime.datetime.now().date()
    if request.method== "get":
        filmlist = film.objects.filter(showDate__lte=now).order_by('filmScore')
        notshow_filmlist = film.objects.filter(showDate__gt=now).order_by('-showDate')
        context = {'film_list': filmlist,
                   'noshow_filmlist':notshow_filmlist
                   }
        return render(request,'home.html',context)

    else:
        category=request.POST.get('category')
        if category:
            category_list = film.objects.filter(category=category , showDate__lte=now).order_by('filmScore')
            return render(request,"category.html",category_list)


def autodelete():  #删除过期电影
    now = datetime.datetime.now().date()
    models.film.objects.filter(deleteDate__lt=now).delete()
