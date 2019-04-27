import xadmin
from .models import film,filmscence,order
from xadmin import  views

class filmAdmin(object):
    model_icon = 'fa fa-film'
    list_display = ['filmName', 'filmDName', 'filmAName','category', 'filmScore','showDate','deleteDate','total']
    search_fields = ['filmName', 'filmDName', 'showDate', 'category','deleteDate']
    list_filter = ['filmName', 'filmDName','showDate','deleteDate','category']
    readonly_fields = ('evaluateNum','filmScoreUser')
    show_detail_fields = ['filmName']
    exclude=['filmSum','evaluateNum']
    list_editable=['showDate','deleteDate']

xadmin.site.register(film, filmAdmin)



class filmscenceAdmin(object):
    model_icon='fa fa-calendar'
    list_display=['dateTime','filmName','price','money']
    search_fields=['dateTime','filmName']
    list_filter = ['dateTime', 'filmName']
    show_detail_fields = ['dateTime']
    readonly_fields=['seat']
    list_editable = ['filmName','price']
    relfield_style = 'fa-ajax'
    # data_charts = {
    #     "场次": {'title': u"场次", "x-field": "dateTime", "y-field": ("money"),},
    # }
xadmin.site.register(filmscence, filmscenceAdmin)


class orderAdmin(object):
    model_icon = 'fa fa-money'
    list_display = ['orderId', 'filmName', 'seat','dateTime','userName','order_time','order_m']
    search_fields = ['orderId', 'filmName','dateTime','userName']
    list_filter = ['dateTime', 'filmName']
    readonly_fields=['orderId','filmName','seat','dateTime','userName','order_m','order_time']
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