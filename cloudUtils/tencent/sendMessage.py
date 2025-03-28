from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models
from djangoTest import settings


def sendsms(phone, code, template_id="1339884"):
    """
                1.注册腾讯云，开通腾讯云短信
                2.创建应用
                    SDK APPID = 1400646716
                3.申请签名（个人：公众号）
                    ID   名称
                    447042	研Share公众号
                4.申请模板
                    ID   名称
                    1339884	普通短信
                5.申请腾讯云API
                    SecretId:AKIDa4SedXu9C1e9SXP5e1qcFfrumUzGQRHx
                    SecretKey:d5KMCrmU0KSPwaBbEpFXiiV9xd9RcfV5
                6.调用相关接口去发送短信
                    SDK，写好的工具
                30s发送一条
            """
    try:
        phone = "{}{}".format("+86", phone)
        cred = credential.Credential(settings.SECRETID, settings.SECRETKEY)
        client = sms_client.SmsClient(cred, settings.TENCENT_CITY)
        req = models.SendSmsRequest()
        req.SmsSdkAppid = settings.TENCENT_APP_ID
        req.Sign = settings.TENCENT_SIGN
        req.TemplateID = template_id
        req.PhoneNumberSet = [phone]
        req.TemplateParamSet = [code, ]
        resp = client.SendSms(req)
        if resp.SendStatusSet[0].Code == 'Ok':
            return True
    except TencentCloudSDKException as err:  # 网络异常
        print(err)
