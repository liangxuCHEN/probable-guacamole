from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


# Create your models here.
class User(AbstractUser):
    AGENT = 1
    ClIENT = 2
    EMPLOYEE = 3
    USER_TYPE_CHOICES = [
        (AGENT, '代理商'),
        (ClIENT, '客户'),
        (EMPLOYEE, '员工')
    ]

    phone = models.CharField(max_length=20, unique=True, db_index=True, null=True, blank=True, verbose_name='手机号')
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, verbose_name='用户类型', default=EMPLOYEE)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class WechatProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wechat_profile', verbose_name='微信用户')
    wx_openid = models.CharField(max_length=50, unique=True, db_index=True, null=True, blank=True, verbose_name='微信OpenID')
    wx_unionid = models.CharField(max_length=50, unique=True, db_index=True, null=True, blank=True, verbose_name='微信UnionID')
    wx_nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='微信昵称')
    wx_avatar = models.URLField(max_length=255, null=True, blank=True, verbose_name='微信头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'

    def __str__(self):
        return f"{self.user.username}'s Wechat Profile"
