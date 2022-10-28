from django.contrib import admin
from .models import LoginUser
# Register your models here.
class LoginUserModelAdmin(admin.ModelAdmin):
    list_display = ['id','login_phone','nicky_name']
    fields = ('login_phone','nicky_name')   #form表单显示内容


admin.site.register(LoginUser,LoginUserModelAdmin)