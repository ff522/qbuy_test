from django.db import models

# Create your models here.
# from goods.models import GoodsModel


class ActiveModel(models.Model):
    title=models.CharField(verbose_name='活动名称', max_length=30)
    start_time = models.CharField(verbose_name='活动开始时间',max_length=20)
    end_time= models.CharField(verbose_name='活动结束时间',max_length=20)
    img1=models.ImageField(verbose_name='活动图片1',upload_to='actives', null=True, blank=True)

    def __str__(self):
        return self.title


    class Meta:
        db_table='t_actives'
        verbose_name=verbose_name_plural='活动信息表'


class ActiveGoodsModel(models.Model):
    #活动id  <外键 ForeignKey(指向ActiveModel)>
    #商品id  <外键 ForeignKey(指向Goods)>
    #折扣 rate   Float类型
    #这是一个关联 商品和活动的第三方表,用于建立他们之间的多对多关系

    active=models.ForeignKey(ActiveModel,related_name='actives',on_delete=models.SET_NULL,verbose_name='活动名称',null=True,blank=True)
    goods=models.ForeignKey('goods.GoodsModel',related_name='goods',on_delete=models.SET_NULL,verbose_name='商品名',null=True,blank=True)
    rate=models.FloatField(verbose_name='折扣',default=0.88)


    @property
    def rate_price(self):
        return self.rate * float(self.goods.price)


    def __str__(self):
        return self.active.title+":"+self.goods.name


    class Meta:
        db_table='t_actives_goods'
        verbose_name=verbose_name_plural='活动商品信息表'
