from __future__ import unicode_literals
from .models import order, film, filmscence,UserProfile,daily
from django.shortcuts import render
import random
import re
import datetime
from django.shortcuts import redirect
from django.contrib import auth
from django.db import models
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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


def film_Detail(request,filmName):    # 电影详情页
    now = datetime.datetime.now()
    if request.method == "get":
        return render(request, 'film/detail.html')
    else:
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
        dateTime = datetime.datetime.strptime(dateTime, "%Y年%m月%d日 %H:%M") #转化时间格式
        date_ex = str(dateTime)[0:10]
        date_ex=datetime.datetime.strptime(date_ex,"%Y-%m-%d")
        filmscences = filmscence.objects.get(dateTime=dateTime) #寻找相应电影
        filmName=filmscences.filmName.filmName
        str_seatList = filmscences.seat
        seatList = str_seatList.split(',')
        int_seatList = []
        for n in seatList:
            int_seatList.append(int(n))
        if seat:
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
            if user_money<0:
                return HttpResponse(0)
            films_r=filmscence.objects.get(pk=dateTime)
            str_seatList_r = films_r.seat
            seatList_r = str_seatList_r.split(',')
            int_seatList_r = []
            for n in seatList_r:
                int_seatList_r.append(int(n))
            for n in int_seat:
                if n in int_seatList_r:
                    return HttpResponse(filmName)
            seatList_r = seatList_r + seat
            str_seatList_r = ','.join(str(i) for i in seatList_r)
            UserProfile.objects.filter(pk=request.user.id).update(money=user_money)
            filmscence.objects.filter(dateTime=dateTime).update(seat=str_seatList_r)
            remains=films_r.remain-1
#进程加锁，成功解决并发问题
            filmscence.objects.filter(dateTime=dateTime).update(remain=remains)
            film_m=films_r.money+money
            filmscence.objects.filter(dateTime=dateTime).update(money=film_m)
            try:
                date_m = daily.objects.get(date=date_ex)
                date_money = date_m.money + money
                daily.objects.filter(date=date_ex).update(money=date_money)
            except:
                date_m=daily()
                date_m.date=date_ex
                date_m.money=money
                date_m.save()
            order_insert = order()
            order_insert.order_m=money
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
        dateTime = datetime.datetime.strptime(dateTime, "%Y年%m月%d日 %H:%M")  # 转化时间格式
        filmscences = filmscence.objects.get(dateTime=dateTime)
        filmName = filmscences.filmName.filmName
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
    if request.method == "POST":   #根据搜索项搜索表单
        selectOne = request.POST.get("selectOne")
        searchCont = request.POST.get("searchCont")
        if selectOne == '0':#利用电影名进行搜索
            film_search= film.objects.filter(filmName__contains=searchCont)
        elif selectOne=='1':#利用导演名进行搜索
            film_search = film.objects.filter(filmDName__contains=searchCont)
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
    if request.method == "get":
        return render(request, 'film/my.html')
    else:
        card = request.POST.get('card')   # 获取目前银行卡号
        userid = request.user.id
        orders = order.objects.filter(userName_id=userid)
        userm = UserProfile.objects.get(pk=userid)
        if card:
            if len(str(card))==10:
                money = userm.money
                money = int(money) + 100
                UserProfile.objects.filter(pk=userid).update(money=money)
                return HttpResponse(1)
            else:
                return HttpResponse(0)
        else:
            t1 = loader.get_template('film/my.html')
            for n in orders:
                flag = 1
                n.seats=""
                for m in n.seat:
                    if(m>='1' and m<='9'):
                        if(flag==1):
                            flag=0
                            n.seats=n.seats+m+"行"
                        else:
                            flag=1
                            n.seats=n.seats+m+"座        "
            context = {'orders': orders ,
                       'user': userm
             }
            return HttpResponse(t1.render(context))
