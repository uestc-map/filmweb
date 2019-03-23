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
        filmName_search=request.POST.get('filmName_search')
        if filmName_search: #如果用户是搜索电影名
            request.session['filmName_search']=filmName_search
            return redirect('film/namesearch')
        filmDName_search = request.POST.get('filmName_search')
        if filmDName_search: #如果用户是搜索导演名
            request.session['filmDName_search']=filmDName_search
            return redirect('film/Dnamesearch')
    else:
        filmlist = film.objects.filter(showDate__lte=now)   #正在热映电影排行榜
        notshow_filmlist = film.objects.filter(showDate__gt=now) #即将上映榜单
        t1 = loader.get_template('film/index.html')
    # 出错
        if request.user.is_authenticated:
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


def film_Detail(request):    #电影详情页
    if request.method == "get":
        return render(request, 'film/detail.html')
    elif request.method == 'post':
        dateTime=request.POST.get("dateTime")    #如果用户点击买票按钮，则将其选择的场次写入session中
        request.session['film_dateTime']=dateTime
        if not request.user.is_authenticated():
            redirect('film/login')   #如果用户未登录，则重定向到登录页
        return redirect('film/buy') #重定向到买票页面
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


@login  #只有登录才可进入
def buy(request):#电影购票页面
    filmeName=request.session['film_detail_name']   #从session中获得电影名与场次信息
    dateTime= request.session['film_dateTime']
    seat=request.POST.get("seat")
    if not seat:  #页面初始化，而非返回买票信息
        t=loader.get_template('film/buy.html')
        seatList = filmscence.objects.filter(filmName__exact=filmeName, dateTime=dateTime)
        film_buy_detail=film.objects.filter(filmeName__exact=filmeName)
        context={
            'seatList':seatList, #已售座位列表
            'film_buy_detail':film_buy_detail  #返回电影详细信息
        }
        return HttpResponse(t.render(context))
    else:   #页面返回的是买票信息
        order_insert = order()
        order_insert.filmName = filmeName
        order_insert.seat = seat
        order_insert.datetime = datetime
        order_insert.userId_id = User.objects.get(userId="userId")
        while True:
            orderId_test = random(0, 1000000000)   #随机生成订单号并检测是否重复
            try:
                orderId_exist = order.objects.get(orderId=orderId_test)
            except Exception as e:
                orderId_exist = None
            if not orderId_exist:
                break
        order_insert.orderId = orderId_test
        order_insert.save()
        return redirect('film/index')  #买票成功，返回主页


def namesearch(request):   #电影名称搜索
    if request.method == "get":
        return render(request, 'film/namesearch.html')
    elif request.method == 'post':
        filmName = request.POST.get('filmName')
        if filmName:  # 如果用户点击某电影详情
            request.session['film_detail_name'] = filmName
            return redirect('film/detail.html')
    else:
        filmName_search = request.session['filmName_search']  # 从session获得当当前电影搜索名
        filmName_searchlist = film.objects.filter(filmName=filmName_search)
        t1 = loader.get_template('film/namesearch.html')
        if request.user.is_authenticated():
            user_active = 1
        else:
            user_active = 0
        context = {'filmName_searchlist': filmName_searchlist,
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))


def Dnamesearch(request):  #导演名称搜索
    if request.method == "get":
        return render(request, 'film/Dnamesearch.html')
    elif request.method == 'post':
        filmName = request.POST.get('filmName')
        if filmName:  # 如果用户点击某电影详情
            request.session['film_detail_name'] = filmName
            return redirect('film/detail.html')
    else:
        filmDName_search = request.session['filmDName_search']  # 从session获得当当前电影搜索名
        filmDName_searchlist = film.objects.filter(filmName=filmDName_search)
        t1 = loader.get_template('film/Dnamesearch.html')
        if request.user.is_authenticated():
            user_active = 1
        else:
            user_active = 0
        context = {'filmDName_searchlist': filmDName_searchlist,
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))


def filmlist_more(request):#点击热榜更多
    now = datetime.datetime.now().date()
    if request.method == "get":
        return render(request, 'film/filmlist.html')
    elif request.method == 'post':
        filmName = request.POST.get('filmName')
        if filmName:  # 如果用户点击某电影详情
            request.session['film_detail_name'] = filmName
            return redirect('film/detail.html')
    else:
        filmlist_more = film.objects.filter(showDate__lte=now) #所有已经上映的电影
        t1 = loader.get_template('film/filmlist.html')
        if request.user.is_authenticated():
            user_active = 1
        else:
            user_active = 0
        context = {'filmlist_more': filmlist_more,
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))


def notshow_filmlist_more(request):#点击即将上映更多
    now = datetime.datetime.now().date()
    if request.method == "get":
        return render(request, 'film/nofilmlist.html')
    elif request.method == 'post':
        filmName = request.POST.get('filmName')
        if filmName:  # 如果用户点击某电影详情
            request.session['film_detail_name'] = filmName
            return redirect('film/detail.html')
    else:
        nofilmlist_more = film.objects.filter(showDate__gt=now) #所有未上映的电影
        t1 = loader.get_template('film/nofilmlist.html')
        if request.user.is_authenticated():
            user_active = 1
        else:
            user_active = 0
        context = {'nofilmlist_more': nofilmlist_more,
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))

def autodelete():  #删除过期电影
    now = datetime.datetime.now().date()
    models.film.objects.filter(deleteDate__lt=now).delete()

