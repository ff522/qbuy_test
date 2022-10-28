import re

from django.test import TestCase

# Create your tests here.


path='/admin/'
print(re.match(r'/user/regist/[\d]*|/admin/.?',path))