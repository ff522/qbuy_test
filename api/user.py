# user相关api接口都在这
from rest_framework import serializers, viewsets


from user.models import LoginUser


# 序列化类---提供给给api视图类使用
class UserModelSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = LoginUser  # 指定  模型
        fields = ('id','login_phone', 'nicky_name') # (模型内)字段选择


# 最终提供api数据的接口视图 view 类(查询结果集视图 )
class UserApiView(viewsets.ModelViewSet):
    queryset = LoginUser.objects.all()  # 提供查询结果集(数据库查询结果)
    serializer_class = UserModelSerializer  # 指定数据转化的序列化类

