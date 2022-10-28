import re

from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


# 验证是否登录的中间件
from QBuyPro import settings


class CheckLoginMiddleware(MiddlewareMixin):
    def process_request(self, request:HttpRequest):
        # 从请求到路由urls过程,触发此函数
        # print('------判断登录状态------------', 'process_request')
        # print(request.path, request.COOKIES)
        import logging
        path=request.path

        ip=request.META.get("REMOTE_ADDR")

        msg='---访问ip:%s,访问路径:%s'%(ip,path)

        #'django'  是setting.py里面日志记录器的名称
        logger=logging.getLogger('my_logger')
        # logger.debug('debug日志')
        # logger.warning("THIS ONE IS")   #记录警告级别日志
        logger.info(msg)                #记录 info级别日志




        if  request.path  not in  [reverse('user:login'),reverse('user:img_code'),'/user/code','/user/reg/']  and re.match(r'/user/regist/[\d]*|/admin/.+|/active/.*qbuy_api/[\d]+|/api.*|',request.path) ==None:

            if not request.COOKIES.get('token'):
                 return HttpResponse('''<p>请先登录,三秒后将自动跳转回 <a href='/user/login'>登录页面</a>
            </p>
            <script>
            setTimeout(()=>{
            open("/user/login")
            
            },3000)
            
            
            </script>
            
            
            ''')


     # def process_view(self, *args):
    #     request=args[0]
    #以下只是举例不同的钩子函数(本中间件暂时用不到,注释掉)

    # def process_view(self, request,callback,callback_args,callback_kwargs):
    #     # 从请求到路由urls过程,触发此函数
    #     #参数里面的callback是接下来要调用的view函数
    #     callback_kwargs['新加参数']=1  #在这里可以新加参数,传递给之后的view函数
    #
    #     #后面是view函数的两个参数
    #     print('------判断登录状态------------', 'process_view')
    #     print(request.path, request.COOKIES)
    #
    # def process_response(self, request, response):
    #
    #
    #     ''' 因为这个钩子函数位于 视图函数到django响应数据时,/
    #         即返回HttpResponse对象后,因此参数有response,意味着这个函数可以对响应对象进行处理'''
    #     print('------判断登录状态------------', 'process_response')
    #    #注意此钩子函数需要返回  response
    #     return response
    # def process_exception(self,request,exception):
    #     print('异常处理中间件')
    #
    #     return HttpResponse('服务器异常%s'%(exception))