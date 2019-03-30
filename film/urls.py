from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import  settings

import re
app_name = 'film'
urlpatterns = [
    url(r"^film/register/$", views.register_User),
    url(r"^film/login/$", views.login),
    url(r"^film/search/$", views.film_search),
    url(r"^film/home/$", views.home_page),
    url(r"^film/detail/$", views.film_Detail),
    url(r"^film/logout/$", views.log_out),
    url(r"^film/my/$", views.my),
    url(r"^film/grade/$",views.film_grade)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

