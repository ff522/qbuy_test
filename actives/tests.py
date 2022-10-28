import io
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QBuyPro.settings')
# hellodjango  为项目的名称,也是 setiings.py所在的项目主文件夹的名称
django.setup()

# from api.user import UserModelSerializer
#
#
# from actives.models import ActiveModel
# from user.models import LoginUser
#
# a=ActiveModel.objects.filter(pk=1)
# print(a)
# print(LoginUser.objects.filter(nicky_name__contains='ff'))
# s1=UserModelSerializer(LoginUser.objects.filter(nicky_name__contains='ff'),many=True)
# s2=UserModelSerializer(LoginUser.objects.all(),many=True)
#
# print(s1.data)
# print(s2.data)
#
#
# from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
# json_content=JSONRenderer().render(s1.data)  #渲染成json数据
# print(json_content)
#
# #将已渲染的json数据烦序列化(此步操作一般用于接收其他地方传递过来的json数据,将其反序列化为python可以理解的对象)
#
# #转化为 io stream流  (一般不需要此步操作)
# stream=io.BytesIO(json_content)
# python_content=JSONParser().parse(stream)
#
# print(type(python_content))


from django.contrib.auth.models import User  # 系统admin内的用户模型
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password

# 首先验证用户

# login_user=User.objects.filter(username='ff520').first()  #用用户名查询数据库中用户
# if check_password('hongye891212',login_user.password):   #验证密码
#
#     print('当前登录用户',login_user.username)
# #生成 token
#     token=Token.objects.create(user=login_user)  #为当前登录用户关联并创建 token
#     print(token)


from redis import Redis
import redis

config={
    'host':'10.8.120.51',
    'port':'6379',
    'db':'2',
    'password':'hongye891212',
     'socket_connect_timeout':1




}


def is_redis_available():
    rs=Redis(**config)
    try:
        rs.client_list()  # getting None returns None or throws an exception
    except ( redis.ConnectionError,redis.exceptions.TimeoutError):
        return False
    return True

print(is_redis_available())