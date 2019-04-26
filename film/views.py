from __future__ import unicode_literals
from .models import order, film, filmscence,UserProfile
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
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import string

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
            user_email = UserProfile.objects.get(email__exact=userEmail)
        except Exception as e:
            user_email = None
        if user_email:
            return render(request, 'film/register.html',{'errmsg':'邮箱已被使用'})

        try:
            user_name=UserProfile.objects.get(username__exact=userName)
        except Exception as e:
            user_name=None
        if user_name:
            return render(request, 'film/register.html',{'errmsg':'用户名已被使用'})


        pass_len=len(str(password))
        if not (re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+', password)) or (pass_len<6):
            return render(request, 'film/register.html', {'errmsg': '密码长度小于6位！'})

        user = UserProfile.objects.create_user(username=userName,password=password,email=userEmail,first_name=0)
        user.save()
        # user_profile = UserProfile(user=user)
        # user_profile.save()
        return redirect("/film/login/")
    elif request.method == "GET":
        return render(request, 'film/register.html')


def login(request):
    if request.method == "POST":
        userName_login= request.POST.get("userName",None)
        password_login=request.POST.get("password",None)
        if not all([userName_login,password_login]):
            return render(request, "film/login.html", {"errmsg": "账号信息不全"})
        user_login = auth.authenticate(username=userName_login, password=password_login)
        if user_login is None:
            return render(request, "film/login.html", {"errmsg": "用户名或密码错误"})
        else:
            auth.login(request, user_login)
            return redirect("/film/home/")

    else:
        return render(request, 'film/login.html')


def home_page(request): #主页
    now = datetime.datetime.now().date()
    if request.method == "get":
        return render(request, 'film/home.html')
    else:
        # category = request.POST.get('category')    #如果用户点击的是电影分类，前端传参名为category，值为分类名
        # if category:
        #     request.session['category_name'] = category  #写入session中
        #     return redirect("film/category.html")
        # filmName = request.POST.get('filmName')
        # if filmName:        #如果用户点击某电影详情，前端传参名为filmName,值为电影名
        #     filmName.replace(' ', '')
        #     request.session['film_detail_name'] = filmName #写入session中
        #     # return redirect('/film/detail/')
        filmlist = film.objects.filter(showDate__lte=now)   #正在热映电影排行榜
        notshow_filmlist = film.objects.filter(showDate__gt=now) #即将上映榜单
        t1 = loader.get_template('film/home.html')
        if (request.user.is_authenticated==True):
            user_active = 1
        else:
            user_active = 0
        context = {'film_list': filmlist,
                   'noshow_filmlist': notshow_filmlist,
                   'user_active': user_active     #用户是否登录
                   }
        return HttpResponse(t1.render(context))


# def category(request):    #电影分类页
#     now = datetime.datetime.now().date()
#     if request.method == "get":
#         return render(request, 'film/category.html')
#     elif request.method == 'post':
#         filmName = request.POST.get('filmName')
#         if filmName:  # 如果用户点击某电影详情
#             request.session['film_detail_name'] = filmName
#             return redirect('film/detail.html')
#     else:
#         category = request.session.get('category_name') #从session获得当前分类名
#         category_list = film.objects.filter(category__exact=category, showDate__lte=now)
#         t1 = loader.get_template('film/category.html')
#         if (request.user.is_authenticated==True):
#             user_active = 1
#         else:
#             user_active = 0
#         context = {'category_list': category_list,
#                    'user_active': user_active  # 用户是否登录
#                    }
#         return HttpResponse(t1.render(context))


def film_Detail(request,filmName):    # 电影详情页
    now = datetime.datetime.now()
    if request.method == "get":
        return render(request, 'film/detail.html')
    else:
        # film_buy_name = request.POST.get('film_buy_name')
        # if film_buy_name:    #如果用户买票
        #     dateTime = request.POST.get("dateTime")    #如果用户点击买票按钮，则将其选择的场次写入session中
        #     request.session['film_buy_dateTime'] = dateTime
        #     request.session['film_buy_name']=film_buy_name
        #     return redirect("film/Cseats.html")
        request.session['film_detail_name'] = filmName   # 从session获得当前电影名
        if filmName.find(' ') >= 0:
            filmName = filmName.replace(' ', '')
        film_detail = film.objects.filter(filmName__exact=filmName)
        filmscences = filmscence.objects.filter(filmName__exact=filmName, dateTime__gt=now)
        t1 = loader.get_template('film/detail.html')
        if (request.user.is_authenticated == True):
            user_active = 1
        else:
            user_active = 0
        context = {'film_detail': film_detail,
                   'filmscences': filmscences,    #场次信息
                   'user_active': user_active  # 用户是否登录
                   }
        return HttpResponse(t1.render(context))


@login_required
def film_grade(request):
    userid = request.user.id
    filmName = request.session.get('film_detail_name')
    filmName = filmName.replace(' ', '')
    Score = float(request.POST.get("num"))
    film_c = film.objects.get(filmName=filmName)
    filmScoreUser =film_c.filmScoreUser#取出打过分的用户的id,形式为1,2,3
    print(filmScoreUser)
    filmScoreUser =filmScoreUser.split(',')     #根据‘，’对字符串进行切片
    int_filmScoreUser=[]
    for n in filmScoreUser:
        int_filmScoreUser.append(int(n))#转变成数字，进行比较
    for n in int_filmScoreUser:
        if userid == n:
            return redirect("/film/detail/"+filmName+"")
    int_filmScoreUser.append(userid) #将用户加入打分列表
    str_filmasaoreUser=','.join(str(i) for i in int_filmScoreUser)#转成字符串格式存入数据库
    filmScore = film_c.filmScore
    filmNum = film_c.evaluateNum
    filmScore = (filmScore * filmNum + Score) / (filmNum + 1)
    filmNum += 1
    film.objects.filter(filmName=filmName).update(filmScore=filmScore)
    film.objects.filter(filmName=filmName).update(evaluateNum=filmNum)
    film.objects.filter(filmName=filmName).update(filmScoreUser=str_filmasaoreUser)
    return redirect("/film/detail/"+filmName+"")


@login_required
def buy(request, dateTime):
    if request.method == "POST":
        seat = request.POST.get("seatlist")
        filmName = request.session.get('film_detail_name')
        dateTime = datetime.datetime.strptime(dateTime, "%Y年%m月%d日 %H:%M") #转化时间格式
        filmscences = filmscence.objects.get(dateTime=dateTime, filmName=filmName) #寻找相应电影
        remain_p=filmscences.remain
        str_seatList = filmscences.seat
        seatList = str_seatList.split(',')
        int_seatList = []
        for n in seatList:
            int_seatList.append(int(n))
        if seat:
            str_seatList = str_seatList + seat
            seat = seat[1:]
            seat = seat.split(',')
            num = 0
            int_seat=[]
            for n in seat:
                num = num + 1
                int_seat.append(int(n))
            money = num * filmscences.price
            user_buy = UserProfile.objects.get(pk=request.user.id)
            user_money = user_buy.money - money
            if user_money<=0:
                return HttpResponse(0)
            UserProfile.objects.filter(pk=request.user.id).update(money=user_money)

            remains=filmscences.remain-1
            if filmscence.objects.filter(dateTime=dateTime,remain=remain_p).update(seat=str_seatList)==False:
                return HttpResponse(2)
#进程加锁，成功解决并发问题
            filmscence.objects.filter(dateTime=dateTime).update(remain=remains)

            order_insert = order()
            order_insert.filmName = film.objects.get(pk=filmName)
            order_insert.seat = int_seat  # 传回的座位信息用‘,’隔开
            order_insert.dateTime = filmscences
            order_insert.userName_id = request.user.id
            while True:
                orderId_test = random.randint(0, 999999999)  # 随机生成订单号并检测是否重复
                try:
                    orderId_exist = order.objects.get(orderId=orderId_test)
                except Exception as e:
                    orderId_exist = None
                if not orderId_exist:
                    break
            orderId_test=str(orderId_test).zfill(10)
            orderId_test=orderId_test
            order_insert.orderId = orderId_test
            order_insert.save()
            filmt=film.objects.get(pk=filmName)
            money=money+filmt.total
            film.objects.filter(pk=filmName).update(total=money)
            return HttpResponse(1)  # 买票成功，返回主页
        else:
            int_seatList.sort()
            return HttpResponse(int_seatList)
    else:
        #页面进入刷新
        pass
        filmName = request.session.get('film_detail_name')
        dateTime = datetime.datetime.strptime(dateTime, "%Y年%m月%d日 %H:%M")  # 转化时间格式
        filmscences = filmscence.objects.get(dateTime=dateTime, filmName=filmName)
        price = filmscences.price
        type = film.objects.get(filmName=filmName).category
        image = film.objects.get(filmName=filmName).image
        context = {
            'filmName': filmName,
            'dataTime': dateTime,
            'price': price,
            'type': type,
            'image':image
        }
        t1 = loader.get_template('film/Cseats.html')
        return HttpResponse(t1.render(context))


def film_search(request): #电影搜索
    now = datetime.datetime.now().date()
    if request.method == "POST":   #根据搜索项搜索表单
        selectOne = request.POST.get("selectOne")
        searchCont = request.POST.get("searchCont")
        # film_category = request.get('film_category')#电影分类
        if selectOne == '0':
            film_search= film.objects.filter(filmName__contains=searchCont)
        elif selectOne=='1':
            film_search = film.objects.filter(filmDName__contains=searchCont)
        # elif film_category: #电影分类
        #     film_search = film.objects.filter(category__exact=film_category)
        if (request.user.is_authenticated==True):
            user_active = 1
        else:
            user_active = 0
        context = {
            'film_search': film_search,
            'user_active': user_active,
        }
        t1 = loader.get_template('film/search.html')
        return HttpResponse(t1.render(context))


def film_searche (request, flag):#更多电影
    now = datetime.datetime.now().date()
    if flag == 0:
        film_searche = film.objects.filter(showDate__lte=now)
    elif flag == 1:
        film_searche = film.objects.filter(showDate__gt=now)
    if (request.user.is_authenticated == True):
        user_active = 1
    else:
        user_active = 0
    context = {
        'film_search': film_searche,
        'user_active': user_active,
    }
    t1 = loader.get_template('film/search.html')
    return HttpResponse(t1.render(context))


def film_searchtype (request , type):
    film_search = film.objects.filter(category=type);
    if (request.user.is_authenticated == True):
        user_active = 1
    else:
        user_active = 0
    context = {
        'film_search': film_search,
        'user_active': user_active,
    }
    t1 = loader.get_template('film/search.html')
    return HttpResponse(t1.render(context))


def autodelete():  #删除过期电影
    now = datetime.datetime.now().date()
    models.film.objects.filter(deleteDate__lt=now).delete()


def log_out(request):
    logout(request)
    return redirect('../login')


# 只有登录才可进入
@login_required
def my(request):
    now = datetime.datetime.now().date()
    if request.method == "get":
        return render(request, 'film/my.html')
    else:
        charge = request.POST.get('charge')
        userid = request.user.id
        orders = order.objects.filter(userName_id=userid)
        userm = UserProfile.objects.get(pk=userid)
        if charge:
            if len(str(charge))==10:
                money=userm.money
                money=int(money)+100
                UserProfile.objects.filter(pk=userid).update(money=money)
                context = {'orders': orders,  # 用户是否登录
                           'errmsg': '成功充值100元',
                           'user':userm
                           }
                return render(request, 'film/my.html',context)
            else:
                context = {'orders': orders, # 用户是否登录
                           'errmsg': '充值卡号错误',
                           'user': userm
                           }
                return render(request, 'film/my.html', context)
        else:
            t1 = loader.get_template('film/my.html')
            context = {'orders': orders , # 用户是否登录
                       'user': userm
             }
            return HttpResponse(t1.render(context))

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

# def filmlist_more(request):#点击热榜更多
#     now = datetime.datetime.now().date()
#     if request.method == "get":
#         return render(request, 'film/filmlist.html')
#     elif request.method == 'post':
#         filmName = request.POST.get('filmName')
#         if filmName:  # 如果用户点击某电影详情
#             request.session['film_detail_name'] = filmName
#             return redirect('film/detail.html')
#     else:
#         filmlist_more = film.objects.filter(showDate__lte=now) #所有已经上映的电影
#         t1 = loader.get_template('film/filmlist.html')
#         if (request.user.is_authenticated==True):
#             user_active = 1
#         else:
#             user_active = 0
#         context = {'filmlist_more': filmlist_more,
#                    'user_active': user_active  # 用户是否登录
#                    }
#         return HttpResponse(t1.render(context))
#
#
# def notshow_filmlist_more(request):#点击即将上映更多
#     now = datetime.datetime.now().date()
#     if request.method == "get":
#         return render(request, 'film/nofilmlist.html')
#     elif request.method == 'post':
#         filmName = request.POST.get('filmName')
#         if filmName:  # 如果用户点击某电影详情
#             request.session['film_detail_name'] = filmName
#             return redirect('film/detail.html')
#     else:
#         nofilmlist_more = film.objects.filter(showDate__gt=now) #所有未上映的电影
#         t1 = loader.get_template('film/nofilmlist.html')
#         if (request.user.is_authenticated==True):
#             user_active = 1
#         else:
#             user_active = 0
#         context = {'nofilmlist_more': nofilmlist_more,
#                    'user_active': user_active  # 用户是否登录
#                    }
#         return HttpResponse(t1.render(context))