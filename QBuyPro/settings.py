"""
Django settings for QBuyPro project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(=39^!c%-uapmedhw!q)3&jq@2k^&mfx*hbm0et!1n(0$4_t@c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles','user','goods','order','actives',
    'rest_framework', 'rest_framework.authtoken',



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'middleware.check_login.CheckLoginMiddleware',
]

ROOT_URLCONF = 'QBuyPro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'QBuyPro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django-qbuypro',
        'PASSWORD': 'ae5e3bf9ec791a9a',
        'HOST': '10.8.120.5',
        'PORT': '3306',
        'USER': 'root',

    }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static') ]# static目录位于源根目录下

MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 配置缓存cache
CACHES = {
    'filecache': {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        'LOCATION': os.path.join(f'{BASE_DIR}', 'mycahce'),  # 缓存文件位置
        'TIMEOUT': 300,  # 超时时间
        'OPTIONS': {
            'MAX_ENTRIES': 500,  # 最大条目数
            'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）

        }

    },
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': 'redis://10.8.120.5:6379/6',  # 数据库位置,2为数据库号

        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100
            },
            "PASSWORD": "hongye891212",  # redis连接密码

            "SOCKET_TIMEOUT": 5,
            "SOCKET_CONNECT_TIMEOUT": 5

        }

    }

}

# 配置session存储到缓存中

# SESSION引擎,这里改用 cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# SESSION对应cookie的名字
SESSION_COOKIE_NAME = 'qbuy_session_id'
# session cookie的路径,影响范围
SESSION_COOKIE_PATH = '/'
# session _cookie的持续时间
SESSION_COOKIE_AGE = 1209600  # 默认为2周

# session采用的缓存方式的名称
SESSION_CACHE_ALIAS = 'default'


##配置django日志
LOGGING = {
    'version': 1.0,  # 版本号

    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置,默认为fale

    # 格式化
    'formatters': {

        # 格式化1:名称自定
        'base': {
            # format 字符串格式化
            'format': '[Log_Time: %(asctime)s ,Log_Name: %(name)s],modules:%(module)s,function:%(funcName)s,Log_Message:%(message)s,log_leverl:%(levelname)s',
            'datefmt': '"%Y年%m月%d日 %H时%M分%S秒'

        }

    },
    # 日志处理器
    'handlers': {
        # 名称自定
        'inf-out': {
            'class': 'logging.StreamHandler',  # 只显示在终端窗口
            'level': 'DEBUG',  # 处理的日志级别
            'formatter': 'base'

        },

        'file': {'class': 'logging.FileHandler',  # 记录到文件
                 'level': 'INFO',  # 处理的日志级别
                 'formatter': 'base',
                 'filename': os.path.join(f'{BASE_DIR}', 'logs', 'commom.log'),
                 'encoding': 'utf-8'  # 文件s编码格式
                 },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(f'{BASE_DIR}', 'logs', 'all.log'),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 10,  # 文件大小
            'encoding': 'utf-8',  # 文件s编码格式
            'backupCount': 5,  # 备份份数
            'formatter': 'base',  # 使用哪种formatters日志格式
        },
        # 上面两种写入日志的方法是有区别的，前者是将控制台下输出的内容全部写入到文件中，这样做的好处就是我们在views代码中的所有print也会写在对应的位置
        # 第二种方法(注意主要是引用的类不同)就是将系统内定的内容写入到文件，具体就是请求的地址、错误信息等

    },

    # 日志记录器
    'loggers': {
        'django.server': {
            'handlers': ['file','default','inf-out'],
            'level': 'DEBUG',  #开发测试,所有日志都应该显示
            'propagate': False

        },  # django.server 应该是控制台输出的默认日志logger;这里把其 记录级别调高之后,系统自带日志就不会出现在控制台了
        'my_logger': {
            'handlers': ['inf-out', 'file', 'default'],
            'level': 'DEBUG',
            'propagate': False

        }

    }

}



#配置 celery选项

CELERY_IMPORTS=('actives.tasks',)   #注意是元组,逗号不要忘了


#配置celery使用的redis数据库; 用户名root其实可以为随意的一个名字
CELERY_BROKER_URL = 'redis://:hongye891212@10.8.120.5:6379/7'
 # 设置存储结果的后台
CELERY_RESULT_BACKEND = 'redis://:hongye891212@10.8.120.5:6379/8'
 # 可接受的内容格式
CELERY_ACCEPT_CONTENT = ["json"]
 # 任务序列化数据格式
CELERY_TASK_SERIALIZER = "json"
 # 结果序列化数据格式
CELERY_RESULT_SERIALIZER = "json"



#配置 rest_framework
REST_FRAMEWORK = {
	 # 配置默认页面大小
	 'PAGE_SIZE': 10,
	 # 配置默认的分页类
	 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

	 'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',  # 时间相关的字段

	 # 配置异常处理器
	 # 'EXCEPTION_HANDLER': 'api.exceptions.exception_handler',

	 # 配置默认解析器
	  'DEFAULT_PARSER_CLASSES': (
	  'rest_framework.parsers.JSONParser',
	  'rest_framework.parsers.FormParser',
	  'rest_framework.parsers.MultiPartParser',
	  ),

	 # 配置默认限流类
	 # 'DEFAULT_THROTTLE_CLASSES': (),

	 # 配置默认认证类
	   'DEFAULT_AUTHENTICATION_CLASSES': (

          'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
           'rest_framework.authentication.TokenAuthentication',  # token认证




	  ),

    #配置默认权限类
     'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),


	 # 配置默认认证类
	 # 'DEFAULT_AUTHENTICATION_CLASSES': (
	 # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
	 # ),

 	    # 关闭api调试界面
	   'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',   # json渲染
           'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览器渲染(生产环境可关掉)
)
}