# user相关api接口都在这
from rest_framework import serializers, viewsets
from actives.models import ActiveModel,ActiveGoodsModel
from api.good import GoodModelSerializer, GoodApiView


class ActiveGoodsModelSerializer(serializers.HyperlinkedModelSerializer):
    goods= serializers.HyperlinkedRelatedField(view_name='goods-detail', read_only=True,many=False)


    class Meta:
        model = ActiveGoodsModel  # 指定  模型
        fields = ('goods','rate')




class ActiveModelSerializer(serializers.HyperlinkedModelSerializer):
    actives=ActiveGoodsModelSerializer(many=True)
    class Meta:
        model = ActiveModel  # 指定  模型
        fields = ('title','start_time','end_time', 'img1','actives') # (模型内)字段选择



# 最终提供api数据的接口视图 view 类(查询结果集视图 )
class ActiveApiView(viewsets.ModelViewSet):
    queryset = ActiveModel.objects.all()  # 提供查询结果集(数据库查询结果)
    serializer_class = ActiveModelSerializer  # 指定数据转化的序列化类


class ActiveGoodsApiView(viewsets.ModelViewSet):
    queryset = ActiveGoodsModel.objects.all()  # 提供查询结果集(数据库查询结果)
    serializer_class = ActiveGoodsModelSerializer  # 指定数据转化的序列化类
