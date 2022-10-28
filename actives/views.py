from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import ActiveModel
from .tasks import qbuy_task
from libs import cache as lib_cache


class ActiveGoodsView(TemplateView):
    template_name = 'goods/goods_list.html'
    def get_context_data(self, **kwargs):

        context=super().get_context_data(**kwargs)
        user_id=self.request.session.get('login_user').get('phone')

        qbuy_good=lib_cache.get_qbuy(user_id)

        pk=kwargs.get('pk')
        if ActiveModel.objects.filter(pk=pk).exists():

            active=ActiveModel.objects.get(pk=pk)
            context['active']=active
        if qbuy_good:
            context['qbuy_good']=int(qbuy_good)
        return context


def qbuy_api(request:HttpRequest,goods_id):
    login_user=request.session.get('login_user')
    if not login_user:

        result={
            'code':100,
            'msg':'当前用户还未登录'




        }

        return  JsonResponse(result)
    else:
        user_id=login_user.get('phone')
        qbuy_task.delay(user_id=user_id,goods_id=goods_id)

        return  JsonResponse({'code':201,'msg':'正在抢购'})



#查询抢购结果
#这里我们自己查询结果,没有接收  tasks里面异步任务的返回
def query_qbuy_api(request:HttpRequest,goods_id):
    login_user=request.session.get('login_user')
    if not login_user:

        result={
            'code':100,
            'msg':'当前用户还未登录'




        }

        return  JsonResponse(result)
    else:
        user_id=login_user.get('phone')
        if lib_cache.exits_qbuy(user_id):

            #首先查询是否有当前用户记录,有的话,再查询qbuy_goods_id
            qbuy_goods_id=lib_cache.get_qbuy(user_id)
            #判断记录中的goods_id与查询goods_id是否相符
            if goods_id==qbuy_goods_id:
                return JsonResponse({
                    'code':200,
                    'msg':'抢购商品%s成功'%(goods_id)})
            else:  #不相符,说明之前已经抢购成功过
                     return JsonResponse({
                        'code':202,
                        'msg':'每天仅限一次抢购,你已经抢过了'


                })

        #如果没有当前用户记录,则继续判断抢购机会还有没有
        elif lib_cache.is_qbuyable():
            return JsonResponse({
                    'code':201,
                    'msg':'正在抢购'})
        else:  #如果已经没有抢购机会,则直接返回抢购失败
             return JsonResponse({
                    'code':300,
                    'msg':'抢购失败,商品已售空'})