from django.contrib import admin
from .models import  order, film, filmscence,UserProfile

# Register your models here.
admin.site.register(order)
admin.site.register(film)
admin.site.register(filmscence)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['money']

admin.site.register(UserProfile, UserProfileAdmin)