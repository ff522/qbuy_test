from django.contrib import admin
from .models import ActiveModel,ActiveGoodsModel
# Register your models here.


class ActiveModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','img1','start_time','end_time']
    fields = ('title','start_time','end_time','img1')   #form表单显示内容

class ActiveGoodsModelAdmin(admin.ModelAdmin):
    list_display = ['id','active','goods','rate']



admin.site.register(ActiveModel,ActiveModelAdmin)
admin.site.register(ActiveGoodsModel,ActiveGoodsModelAdmin)