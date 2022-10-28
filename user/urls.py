from django.urls import path

from user import views
from user.api_login import LoginViewSet

app_name='user'
urlpatterns=[
    # re_path('regist/',views.regist),

    path('reg/', views.reg, name='reg'),

 path('login/', views.login, name='login'),path('logout', views.logout),
path('list', views.list, name='list'),path('code', views.new_code),
    path('imgcode', views.new_img_code, name='img_code'),

 path('user_api', views.user_api, name='user_api'),
    path('user_api/<int:pk>', views.user_detail, name='user_api_detail'),

 path('user_api2', views.User_APIView.as_view(), name='user_api2'),
    path('user_api2/<int:pk>', views.User_detail_ApiView.as_view(), name='user_api2_detail'),

path('user_api_login', LoginViewSet.as_view(), name='api_login'),
]