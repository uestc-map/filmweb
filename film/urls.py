from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import  settings

import re
app_name = 'film'
urlpatterns = [
    # url(r"^film/register/$", views.register_User),
    # url(r"^film/login/$", views.login),
    # url(r"^film/search/$", views.film_search),
    path("search/", views.film_search),
    path("searche/<int:flag>", views.film_searche),
    # url(r"^film/home/$", views.home_page),
    # url(r"^film/detail/$", views.film_Detail),
    # url(r"^film/logout/$", views.log_out),
    # url(r"^film/my/$", views.m
                  # y),
    # url(r"^film/grade/$",views.film_grade),
    path("register/", views.register_User, name="register"),
    path("login/", views.login, name="login"),
    path("home/", views.home_page, name="home"),
    path("detail/", views.film_Detail, name="detail"),
    path("logout/", views.log_out, name="logout"),
    path("grade/", views.film_grade, name="grade"),
    path("buy/<str:dateTime>", views.buy),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

