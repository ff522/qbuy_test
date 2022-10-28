# user相关api接口都在这
from rest_framework import serializers, viewsets



# 序列化类---提供给给api视图类使用
from goods.models import GoodsModel


class GoodModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsModel  # 指定  模型
        fields = ('name','price','info', 'img1') # (模型内)字段选择


class GoodApiView(viewsets.ModelViewSet):
    queryset = GoodsModel.objects.all()  # 提供查询结果集(数据库查询结果)
    serializer_class = GoodModelSerializer  # 指定数据转化的