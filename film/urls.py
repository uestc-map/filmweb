from django.urls import path
from django.conf.urls import url
from . import views

import re
app_name = 'film'
urlpatterns = {
    url(r"^film/register/$", views.register_User),
    url(r"^film/login/$", views.login),


    url(r"^film/index/$", views.index_page),
    url(r"^film/category/$", views.category),
    url(r"^film/detail/$", views.film_Detail),

}

