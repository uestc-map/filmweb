import xadmin
from .models import film,filmscence,order
from xadmin import  views
class filmAdmin(object):
    list_display = ['filmName', 'filmDName', 'filmAName', 'filmScore', 'filmScore','showDate','deleteDate','total']
    search_fields = ['filmName', 'filmDName', 'showDate', 'deleteDate']
    list_filter = ['filmName', 'filmDName','showDate','deleteDate']
    show_detail_fields = ['filmName']
xadmin.site.register(film, filmAdmin)

class filmscenceAdmin(object):
    list_display=['dateTime','filmName','price']
    search_fields=['dateTime','filmName']
    list_filter = ['dateTime', 'filmName']
    show_detail_fields = ['dateTime']
xadmin.site.register(filmscence, filmscenceAdmin)

class orderAdmin(object):
    list_display = ['orderId', 'filmName', 'seat','dateTime','userId']
    search_fields = ['orderId', 'filmName','dateTime','userId']
    list_filter = ['dateTime', 'filmName']
xadmin.site.register(order, orderAdmin)

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title="肥宅电影"
    site_footer="电子科技大学"
    menu_style="accordion"

xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)