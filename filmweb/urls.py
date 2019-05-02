"""filmweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path,re_path
import xadmin
from .settings import MEDIA_ROOT  # 上传媒体加载包
from django.views.static import serve  # 上传媒体加载包
urlpatterns = [
    path('film/', include('film.urls')),
    path('admin/', admin.site.urls),
    path(r'xadmin/',xadmin.site.urls),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),  # 指定上传媒体位置
]
