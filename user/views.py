import json
import os
import re
import uuid
import datetime
import random
from urllib.parse import urlparse

from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from PIL import Image, ImageDraw, ImageFont
from django.core.paginator import Page, Paginator
from requests import Response


from user.models import LoginUser


def login(req: HttpRequest):
    # valid_code=req.session.get('valid_code')

    if req.method == 'POST':
        phone = json.loads(req.body).get('phone')
        code = json.loads(req.body).get('code')
        print('缓存中', cache.get(phone))

        u1 = LoginUser.objects.filter(login_phone=phone).all()

        if u1:

            # 比较session中存储的数据(phone和code)与用户输入的数据
            if all((
                    phone == req.session.get('phone'),
                    code == req.session.get('code')

            )):
                resp = HttpResponse('''<p>恭喜登录成功,三秒后自动跳转 <a href='/user/list'>用户列表</a>
                </p>
                <script>
                setTimeout(()=>{
                open("/user/list" ,target='_self')
                
                },3000)
                
                
                </script>
                
                
                ''')
                # 删除缓存中的code
                cache.delete(phone)

                token = uuid.uuid4().hex

                cache.set(token, phone)
                req.session['login_user'] = {
                    'name': u1[0].nicky_name,

                    'phone': u1[0].login_phone

                }

                resp.set_cookie(key='token', value=token, expires=datetime.datetime.now() + datetime.timedelta(days=14))

                return resp

            resp = HttpResponse('登陆失败,请检查手机号或验证码', status=401)

            return HttpResponse(resp)

        return HttpResponse('''<p>很遗憾,改手机号还未注册,,三秒后自动跳转 <a href='/user/list'>用户注册</a>
                </p>
                <script>
                setTimeout(()=>{
                open("/user/reg" ,target='_self')
                
                },3000)
                
                
                </script>
                
                
                ''')
    elif req.method == 'GET':
        token = req.COOKIES.get('token')
        if token:
            return HttpResponse('''<p>你已经登录,三秒后将自动跳转回 <a href='/user/list'>用户列表</a>
            </p>
            <script>
            setTimeout(()=>{
            open("/user/list" ,target='_self')
            
            },3000)
            
            
            </script>
            
            
            ''')

        return render(req, 'user/login.html', locals())


def logout(req: HttpRequest):
    # 注销成功
    # 删除所有cookie和session信息
    token = req.COOKIES.get('token')

    req.session.clear()  # 删除所有session中信息
    resp = HttpResponse('''
   
    
    <p>注销成功,三秒后将自动跳转回 <a href='/user/login'>登录页面</a>
                </p>
               
              <script>
                setTimeout(()=>{
                open("/user/login" ,target='_self')
                
                },3000)
                
                
                 </script>
                
                
                ''')
    resp.delete_cookie('token')  # 删除cookie

    cache.delete(token)

    return resp


import time
from django.views.decorators.cache import cache_page


def list(req: HttpRequest):
    # 验证是否登录
    # raise Exception('hah 出错了,稍后再来吧')

    return render(req, 'user/list.html')


def new_code(req: HttpRequest):
    # 生成(手机)验证码
    # 随机产生验证码:字母和数字
    code = create_code(5)

    phone = json.loads(req.body).get('phone')
    valid_code = json.loads(req.body).get('valid_code')

    # 来源网页的path

    refer_path = urlparse(req.headers.get('Referer')).path
    print('图形验证码', valid_code)
    print('code', req.session['valid_code'])
    if valid_code != req.session['valid_code']:
        return HttpResponse('图形验证码不正确')
    else:
        if phone:
            if re.match(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$', phone):
                u1 = LoginUser.objects.filter(login_phone=phone).all()

                if not u1 and refer_path == '/user/login/':
                    return HttpResponse('很遗憾,你的手机号还未注册,请点击注册按钮请进行用户注册')
                elif u1 and refer_path == '/user/reg/':
                    return HttpResponse('手机号已经注册,请切换登录页面直接登录')
                else:

                    # 保存到session中
                    req.session['code'] = code
                    req.session['phone'] = phone
                    # 将code保存到 cache中
                    from django.core.cache import cache
                    cache.set(phone, code, timeout=60)  # 保存到缓存,参数格式(key,value)

                    # 向手机发送验证码
                    # from signals import codeSignal
                    # #发送信号
                    # #send() 方法的第一个参数是 sender,其名称可以根据需求自定
                    # #后面跟着的关键字参数,需要根据信号定义时 的参数列表传值
                    # codeSignal.send('new_code',path=req.path,phone=phone,code=code)

                    return HttpResponse('已经向%s发送了验证码,code为%s' % (phone, req.session.get('code')))


            else:
                return HttpResponse('请输入正确格式的手机号')
        else:
            return HttpResponse('手机号不能为空')


def create_code(len):
    code_list = []
    for i in range(10):
        code_list.append(str(i))  # 生成数字
    for i in range(97, 123):  # 此为小写英文字母的ascii值范围
        code_list.append(chr(i))  # 生成小写字母 #chr(ascii)=>字符串
    while True:
        r = random.sample(code_list, len)  # 随机从code_list中取len个字符产生一个列表
        code = ''.join(r)  # 组合成字符串
        if not code.isdigit() and not code.isalpha():  # 判断字符串是否为 字母数字混合

            break
    return code


def new_img_code(req: HttpRequest):
    # 生成图形验证码(使用PIL)

    # 第一步:使用 PIL的IMage生成画布
    bg = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    img = Image.new('RGB', (100, 40), bg)  # 模式,尺寸(单位px),背景颜色

    # 从画布中获取画笔
    draw = ImageDraw.Draw(img, 'RGB')  # 第一个参数为 画布对象,第二个为 模式(画布与画笔模式独立)

    # 创建字体对象和颜色

    font = ImageFont.truetype(font='static/fonts/arial.ttf', size=30)

    # 生成code
    code = create_code(5)
    # 将code 保存到  session中.方便其他视图函数调用
    req.session['valid_code'] = code

    # 开始画内容
    # 循环绘制文本(每个文本使用不同颜色)
    for char in code:
        font_color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        if font_color == bg:
            continue
        xy = (5 + 20 * code.index(char), random.randint(1, 8))

        draw.text(xy, font=font, fill=font_color, text=char)
    draw.line((0, 0), (255, 0, 0), 20)  # 画线
    for i in range(100):  # 画100个点
        xy = (random.randrange(100), random.randrange(40))
        p_color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        draw.point(xy, p_color)
    del draw

    # 画完后,将画布写入内存缓存中
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, 'png')  # 将img保持到buffer中

    # 生成httpresponse对象
    return HttpResponse(content=buffer.getvalue(), content_type='image/png')


def reg(req):
    if req.method == 'POST':
        phone = json.loads(req.body).get('phone')
        code = json.loads(req.body).get('code')
        nicky_name = json.loads(req.body).get('nicky_name')

        print('缓存中', cache.get(phone))

        # 比较session中存储的数据(phone和code)与用户输入的数据
        if all((
                phone == req.session.get('phone'),
                code == req.session.get('code')

        )):
            resp = HttpResponse('''<p>恭喜注册成功,三秒后自动跳转 <a href='/user/list'>用户列表</a>
                </p>
                <script>
                setTimeout(()=>{
                open("/user/list" ,target='_self')
                
                },3000)
                
                
                </script>
                
                
                ''')
            # 删除缓存中的code
            cache.delete(phone)

            print('缓存已删除', cache.get(phone))

            token = uuid.uuid4().hex
            u1 = LoginUser()
            u1.login_phone = phone
            u1.nicky_name = nicky_name
            u1.save()

            cache.set(token, phone)
            req.session['login_user'] = {
                'name': u1.nicky_name,

                'phone': u1.login_phone
            }

            resp.set_cookie(key='token', value=token, expires=datetime.datetime.now() + datetime.timedelta(days=14))

            return resp

        resp = HttpResponse('注册失败,请检查手机号或验证码', status=401)

        return HttpResponse(resp)


    elif req.method == 'GET':
        token = req.COOKIES.get('token')

        if token:
            return HttpResponse('''<p>你已经登录,三秒后将自动跳转回 <a href='/user/list'>用户列表</a>
            </p>
            <script>
            setTimeout(()=>{
            open("/user/list" ,target='_self')
            
            },3000)
            
            
            </script>
            
            
            ''')

        return render(req, 'user/reg.html', locals())


from rest_framework.decorators import api_view
from api.user import UserModelSerializer

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,TokenAuthentication


# 使用restful自定义api_view
@api_view(["GET", "POST"])
def user_api(request):
    if request.method == "GET":
        datas = LoginUser.objects.all()
        # 调用序列化器
        serializer_class = UserModelSerializer(instance=datas, many=True)
        return Response(serializer_class.data)
    elif request.method == "POST":
        ##以下是添加数据,序列化器参数中只需要有 新数据
        serializer_class = UserModelSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()

            # return Response(serializer_class.data)
            return Response(serializer_class.instance)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


# 如果需要看每个条目的详情,还需要加上下面的处理函数
@api_view(["GET", "DELETE", "PUT"])
def user_detail(request, pk):
    try:
        data = LoginUser.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        # 调用序列化器
        serializer_class = UserModelSerializer(data)
        return Response(serializer_class.data)

    elif request.method == "DELETE":
        data.delete()
        print('已删除')
        return Response(status=status.HTTP_204_NO_CONTENT)


    elif request.method == "PUT":
        # 以下是修改已有数据,序列化器器参数中需要有 已经数据模型的实例对象
        # instance
        serializer_class = UserModelSerializer(instance=data, data=request.data)
        serializer_class.get_serializer()
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView


class User_APIView(APIView):
    authentication_classes = (TokenAuthentication, )  #认证类

    permission_classes = (IsAuthenticated,)  #获取授权类

    def get(self, request):
        print(request.user)
        datas = LoginUser.objects.all()

        # 调用序列化器
        serializer_class = UserModelSerializer(instance=datas, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        ##以下是添加数据,序列化器参数中只需要有 新数据
        serializer_class = UserModelSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()

            # return Response(serializer_class.data)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class User_detail_ApiView(APIView):
    def get_object(self, request, pk):
        try:
            return LoginUser.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):

        serializer_class = UserModelSerializer(self.get_object(request, pk))
        return Response(serializer_class.data)

    def delete(self, request, pk):
        self.get_object(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None):
        serializer_class = UserModelSerializer(instance=self.get_object(request, pk), data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
