from django.contrib import admin
from .models import GoodsModel
# Register your models here.


class GoodsModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','info','img1']
    fields = ('name','price','info','img1')   #form表单显示内容


admin.site.register(GoodsModel,GoodsModelAdmin)