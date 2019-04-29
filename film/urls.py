from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import  settings

app_name = 'film'
urlpatterns = [

    path("search/", views.film_search),
    path("searche/<int:flag>", views.film_searche),
    path("searchtype/<str:type>", views.film_searchtype),
    path("my/", views.my),
    path("register/", views.register_User, name="register"),
    path("login/", views.login, name="login"),
    path("home/", views.home_page, name="home"),
    path("detail/<str:filmName>", views.film_Detail),
    path("logout/", views.log_out, name="logout"),
    path("grade/", views.film_grade, name="grade"),
    path("buy/<str:dateTime>", views.buy),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

