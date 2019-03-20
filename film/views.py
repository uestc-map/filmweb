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
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect

def register_User(request):
    if request.method== "POST":
        userEmail= request.POST.get("userEmail",None)
        userName=request.POST.get("userName",None)
        password=request.POST.get("password",None)
        if not all([ userEmail,userName,password]):
            return render(request, 'film/register.html')
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', userEmail):
            return render(request, 'film/register.html', {'errmsg': '邮箱不符合规范'})

        try:
            user_email = User.objects.get(email__exact=userEmail)
        except Exception as e:
            user_email = None
        if user_email:
            return render(request, 'film/register.html',{'errmsg':'邮箱已被使用'})

        try:
            user_name=User.objects.get(username__exact=userName)
        except Exception as e:
            user_name=None
        if user_name:
            return render(request, 'film/register.html',{'errmsg':'用户名已被使用'})


        pass_len=len(str(password))
        if not (re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+',password)) or (pass_len<6):
            return render(request, 'film/register.html', {'errmsg': '密码长度小于6位！'})

        user = User.objects.create_user(username=userName,password=password,email=userEmail)
        user.save()
        return redirect("/film/login/")
    elif request.method == "GET":
        return render(request, 'film/register.html')


def login(request):
    if request.method == "POST":
        userName_login= request.POST.get("userName",None)
        userename_login= request.POST.get("userName",None)
        password_login=request.POST.get("password",None)
        if not all([userName_login,password_login]):
            return render(request, "film/login.html", {"errmsg": "账号信息不全"})
        user_login = auth.authenticate(username=userName_login, password=password_login)
        if user_login is None:
            return render(request, "film/login.html", {"errmsg": "用户名或密码错误"})
        else:
            auth.login(request, user_login)
            return redirect("/film/index/")

    else:
        return render(request, 'film/login.html')


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
        order_insert.userId_id=User.objects.get(userId="userId")
        order_insert.save()
    return render(request, 'insert.html')


# def insert_film(request):
#     if request.method== "POST":
#         film_insert=film()
#         film_insert.filmName= request.POST.get("filmName",None)
#         film_insert.filmDName=request.POST.get("filmDName",None)
#         film_insert.image=request.POST.get("ROUTE",None)  #暂时还不会写
#         film_insert.category=request.POSY.get("category",None)
#         if not all([ film_insert.filmName, film_insert.filmDName, film_insert.Route, film_insert.category]):
#             return render(request, 'insert.html')
#
#         try:
#            film_exist = film.objects.get(filmName=film_insert.filmName)
#         except Exception as e:
#             film_exist = None
#         if film_exist:
#             return render(request, 'insert.html', {'errmsg': '电影已存在'})
#         return render(request, 'insert.html')
#
# def insert_filmscence(request):
#     if request.method== "POST":
#         filmscence_insert=filmscence()
#         filmscence_insert.datetime= request.POST.get("datetime",None)
#         filmscence_insert.filmName_id=film.objects.get(filmName="filmName")
#         try:
#            datetime_exist = filmscence.objects.get(datetime=filmscence_insert.datetime)
#         except Exception as e:
#             datetime_exist = None
#         if datetime_exist:
#             return render(request, 'insert.html', {'errmsg': '该场次已有电影'})
#         return render(request, 'insert.html')
#

def index_page(request): #主页
    now = datetime.datetime.now().date()
    if request.method== "get":
        return  render(request,'film/index.html')

    elif request.method=='post':
        category=request.POST.get('category')    #如果用户点击的是电影分类，前端传参名为category，值为分类名
        if category:
            request.session['category_name']=category  #写入session中
            return redirect("film/category.html")
        filmName=request.POST.get('filmName')
        if filmName:        #如果用户点击某电影详情，前端传参名为filmName,值为电影名
            request.session['film_detail_name']=filmName  #写入session中
            return redirect('film/detail.html')
    else:
        filmlist = film.objects.filter(showDate__lte=now)   #正在热映电影排行榜
        notshow_filmlist = film.objects.filter(showDate__gt=now) #即将上映榜单
        t1 = loader.get_template('film/index.html')
        if request.user.is_authenticated():
            user_active=1
        else:
            user_active=0
        context = {'film_list': filmlist,
                   'noshow_filmlist': notshow_filmlist,
                   'user_active':user_active     #用户是否登录
                   }
        return HttpResponse(t1.render(context))


def category(request):    #电影分类页
    now = datetime.datetime.now().date()
    if request.method == "get":
        return render(request, 'film/category.html')
    elif request.method == 'post':
        filmName = request.POST.get('filmName')
        if filmName:  # 如果用户点击某电影详情
            request.session['film_detail_name'] = filmName
            return redirect('film/detail.html')
    else:
        category = request.session['category_name'] #从session获得当前分类名
        category_list = film.objects.filter(category__exact=category, showDate__lte=now)
        t1 = loader.get_template('film/category.html')
        if request.user.is_authenticated():
            user_active = 1
        else:
            user_active = 0
        context = {'category_list': category_list,
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))


def film_Detail(request):    #电影详情页，应包含买票功能，暂时还没写好
    if request.method == "get":
        return render(request, 'film/detail.html')
    elif request.method == 'post':    #电影买票功能还未完善
        return render(request, 'film/detail.html')
    else:
        filmName = request.session['film_detail_name']#从session获得当前电影名
        film_detail=film.objects.filter(filmName__exact=filmName)
        t1 = loader.get_template('film/detail.html')
        if request.user.is_authenticated():
            user_active = 1
        else:
            user_active = 0
        context = {'category_list': film_detail,
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))

def autodelete():  #删除过期电影
    now = datetime.datetime.now().date()
    models.film.objects.filter(deleteDate__lt=now).delete()
