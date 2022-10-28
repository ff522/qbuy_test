import time

from celery import shared_task
from libs import cache


@shared_task
def qbuy_task(**kwargs):
    goods_id=kwargs.get('goods_id')
    user_id=kwargs.get('user_id')



    #首先 两个id要存在
    if user_id and goods_id:
        time.sleep(5)  #模拟抢购耗时
        #判断是否已经抢完
        if cache.is_qbuyable():
            #继续判断当前用户是否已抢过

            if cache.exits_qbuy(user_id) == False:
                 cache.add_qbuy(user_id,goods_id)

            else:
                 return "%s抢购%s失败,原因:每天限一次"%(user_id,goods_id)


        return "%s库存已空,抢购%s失败"%(user_id,goods_id)
