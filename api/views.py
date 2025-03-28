import re
import json
import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response  # 还只能是大写的Response
from sts.sts import Sts, CIScope, Scope

from .serializer.account import MessageSerializer
from .serializer.account import LoginSerializer
from cloudUtils.tencent.sendMessage import sendsms


class MessageView(APIView):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        1.获取手机号
        2.校验手机号格式
        3.生成随机验证码
        4.验证码发送到手机
        5.把验证码+手机号保留（30s过期）
        """
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({"status": False, "message": "手机格式错误"})
        phone = request.query_params.get('phone')

        def generate_four_digit_string(): # 使用函数生成随机字符串
            import random
            digits = [str(i) for i in range(10)]
            random.shuffle(digits)
            return ''.join(digits[:4])
        random_codes = generate_four_digit_string()
        if not sendsms(phone, random_codes):
            return Response({"status": False, "message": "短信发送失败"})
        print(random_codes)
        from django_redis import get_redis_connection
        conn = get_redis_connection()
        conn.set(phone, random_codes, ex=60)
        return Response({"status": True, "message": "发送成功"})


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        """
        1.校验手机号是否合法
        2.校验验证码，redis是否合理
            -无验证码
            -有验证码，输入有误
            -有验证码，成功
        3.去数据库中获取用户信息（获取/创建）
        4.将一些信息返回给小程序
        """
        print(request.data)
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message': '验证码错误'})
        from api import models
        phone = ser.validated_data.get('phone')
        user_object, flag = models.UserInfo.objects.get_or_create(phone=phone)
        user_object.token = str(uuid.uuid4)
        user_object.save()

        return Response({"status": True, "data": {"token": user_object.token, "phone": phone}})


class CredentialView(APIView):

    def get(self, request, *args, **kwargs):
        from djangoTest import settings
        config = {
            'duration_seconds': 1800,
            'secret_id': settings.SECRETID,
            # 固定密钥
            'secret_key': settings.SECRETKEY,
            # 换成你的 bucket
            'bucket': 'tinyfavor-1303993620',
            # 换成 bucket 所在地区
            'region': 'ap-guangzhou',
            'allow_prefix': "*",
            'allow_actions': [
                # 简单上传
                'name/cos:PostObject',
            ],
        }
        sts = Sts(config)
        response = sts.get_credential()
        print('get data : ' + json.dumps(dict(response), indent=4))
        return Response(response)


