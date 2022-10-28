from django.urls import path,re_path

from actives import views

app_name='actives'
urlpatterns=[
    # re_path('regist/',views.regist),

  path('info/<pk>',views.ActiveGoodsView.as_view(),name='info'),
path('qbuy_api/<goods_id>',views.qbuy_api,name='qbuy'),
  path('query_qbuy_api/<goods_id>',views.query_qbuy_api,name='query_qbuy'),


]

