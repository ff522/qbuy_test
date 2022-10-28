from django.db import models

# Create your models here.
class GoodsModel(models.Model):
    name=models.CharField(verbose_name='商品名', max_length=30)
    price = models.DecimalField(verbose_name='价格',max_digits=10,decimal_places=2)
    info=models.TextField(verbose_name='商品描述')
    img1=models.ImageField(verbose_name='商品图片1',upload_to='goods', null=True, blank=True)

    def __str__(self):
        return self.name


    class Meta:
        db_table='t_goods'
        verbose_name=verbose_name_plural='商品表'