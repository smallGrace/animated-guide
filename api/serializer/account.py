from rest_framework import serializers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .validators import phone_validator
from django.shortcuts import render
from django_redis import get_redis_connection


class MessageSerializer(serializers.Serializer):

    # 短信没有关联的数据库，所以没有使用ModelSerializer，使用的是Serializer
    # 两个校验规则，一个是不能为空，一个是手机格式的正则表达式
    phone = serializers.CharField(label="手机号", validators=[phone_validator, ])  # 方便手机验证校验通用

    # def validate_phone(self, value):
    #     pass


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator, ])
    code = serializers.CharField(label="短信验证码")

    def validate_code(self, value):
        if len(value) != 4:
            raise ValidationError('短信格式错误')
        if not value.isdecimal():
            raise ValidationError('短信格式错误')
        phone = self.initial_data.get('phone')
        conn = get_redis_connection()
        code = conn.get(phone)
        if not code:
            raise ValidationError('验证码过期')
        if value != code.decode('utf-8'):
            raise ValidationError('验证码错误')
        return value