from rest_framework import routers

from api.active import ActiveApiView, ActiveGoodsApiView
from api.good import GoodApiView
from api.user import UserApiView

#声明api路由



api_route=routers.DefaultRouter()


#向api路由中注册我们写的UserApiViewSet类
api_route.register('user',UserApiView)
api_route.register('active',ActiveApiView)
api_route.register('active_goods',ActiveGoodsApiView)
api_route.register('goods',GoodApiView,basename='goods')



