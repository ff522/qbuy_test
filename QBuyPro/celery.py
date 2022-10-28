from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
#为Celery命令设置默认的环境变量。当执行Celery命令时，会自动使用指定的settings作为配置文件，而不必每次执行时都要指定配置文件。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QBuyPro.settings')   #填入 settings.py文件的实际引用位置

# 生成Celery实例，对于Django，只需要一个
app = Celery('QBuyPro')  #这里是填入项目的名称

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

#下面是设置Django项目的settings作为Celery的一部分配置文件。这样你就可以直接将Celery的配置项配置在Django项目的settings文件中，而不必为Celery单独写一个配置文件。但是Celery支持单独定义配置文件。
#至于 namespace='CELERY' ：Django的settings配置文件中，Celery的配置项都以大写的CELERY_开头。当然此项可以不指定，但是为了防止和Django配置项混淆，建议指定。
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
#最佳项目实践是将不同app的task放在不同的task.py模块中。自动加载经过注册的app根目录下的task。app的根目录如下：。这样就不需要配置CELERY_IMPORTS来指定每个app具体task.py路径。
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))