from django.contrib import auth
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class LoginViewSet(APIView):
    '''登录方法'''

    permission_classes = (AllowAny,)      # AllowAny 允许所有用户


    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse({"code": 0,
                                "msg": "用户名或密码不对!"})
        # 删除原有的Token
        old_token = Token.objects.filter(user=user)
        old_token.delete()
        # 创建新的Token
        token = Token.objects.create(user=user)
        return JsonResponse({"code": 0,
                             "msg": "login success!",
                             "username": user.username,
                             "token": token.key})
