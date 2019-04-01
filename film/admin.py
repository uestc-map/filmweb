from django.contrib import admin
from .models import  order, film, filmscence
# Register your models here.
admin.site.register(film)
admin.site.register(filmscence)
admin.site.register(order)