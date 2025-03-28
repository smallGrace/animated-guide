from django.db import models


class UserInfo(models.Model):
    phone = models.CharField(verbose_name='手机号', max_length=11, unique=True)
    token = models.CharField(verbose_name='用户token', max_length=64, blank=True)
# Create your models here.
