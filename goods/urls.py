from django.urls import path,re_path

from goods import views

app_name='goods'
urlpatterns=[
    # re_path('regist/',views.regist),

  path('info/<pk>',views.GoodsView.as_view(),name='info'),


]

