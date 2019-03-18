from django.urls import path
from django.conf.urls import url
from . import views

import re
app_name = 'film'
urlpatterns = [
    url(r"^film/register/$", views.register_User),
    url(r"^film/login/$", views.login),
    url(r"^film/index/$", views.home_page),
]