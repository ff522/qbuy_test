from django.db import models

# Create your models here.

class LoginUser(models.Model):
    login_phone=models.CharField(verbose_name='登陆手机号', max_length=11)
    nicky_name = models.TextField(verbose_name='用户昵称')

    def __str__(self):
        return self.login_phone


    class Meta:
        db_table='t_login_user'
        verbose_name=verbose_name_plural='用户表'


