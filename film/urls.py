from django.urls import path
from django.conf.urls import url
from . import views

import re
app_name = 'film'
urlpatterns = [
    url(r"^film/register/$", views.register_User),
    url(r"^film/login/$", views.login),
<<<<<<< HEAD
    url(r"^film/index/$", views.index_page),
=======
    url(r"^film/index/$", views.home_page),
>>>>>>> 70b725a3a6f3187cbd21444d5e2e7f29ce0a3c10
]