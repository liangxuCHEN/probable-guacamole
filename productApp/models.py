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
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='国家')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='城市')

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


class ProductType(models.Model):
    """产品类型表"""
    name = models.CharField(max_length=100, verbose_name='产品名称')
    model_number = models.CharField(max_length=50, verbose_name='型号')
    specifications = models.TextField(null=True, blank=True, verbose_name='规格')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    warranty_period = models.IntegerField(default=365, verbose_name='保修期(天)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '产品类型'
        verbose_name_plural = '产品类型'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.model_number})"


class Product(models.Model):
    """产品二维码表"""
    STATUS_CHOICES = [
        (1, '已生成'),
        (2, '已出货'),
        (3, '已激活'),
        (4, '维修中'),
        (5, '已报废')
    ]
    
    qrcode_id = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='二维码ID')
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, null=True, blank=True,
        related_name='products', verbose_name='产品类型'
    )
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_products', 
                             limit_choices_to={'user_type': User.AGENT}, verbose_name='代理商')

    shipping_date = models.DateTimeField(null=True, blank=True, verbose_name='出货日期')
    activation_date = models.DateTimeField(null=True, blank=True, verbose_name='激活日期')

    warranty_start_date = models.DateTimeField(null=True, blank=True, verbose_name='保修开始日期')
    warranty_end_date = models.DateTimeField(null=True, blank=True, verbose_name='保修结束日期')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 客户信息：name, phone, city, country, email
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='客户姓名')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='客户电话')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='客户城市')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='客户国家')
    email = models.EmailField(null=True, blank=True, verbose_name='客户邮箱')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.qrcode_id}"
    
    def is_under_warranty(self):
        """检查产品是否在保修期内"""
        if not self.warranty_start_date or not self.warranty_end_date:
            return False
        from django.utils import timezone
        now = timezone.now()
        # 补充时区的处理,系统为东8区
        now = now + timedelta(hours=8)
        return self.warranty_start_date <= now <= self.warranty_end_date
    
    def activate(self):
        """激活产品"""
        if self.status == 2:  # 只有已出货的产品才能激活
            self.activation_date = datetime.now()
            self.warranty_start_date = self.activation_date
            # 根据产品类型设置保修结束日期
            self.warranty_end_date = self.activation_date + timedelta(days=self.product_type.warranty_period)
            self.status = 3  # 更新状态为已激活
            self.save()
            return True
        return False


class OperationRecord(models.Model):
    """操作记录表"""
    OPERATION_CHOICES = [
        (1, '创建产品'),
        (2, '产品出货'),
        (3, '产品激活'),
        (4, '维修登记'),
        (5, '维修完成'),
        (6, '报废处理')
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='operation_records', verbose_name='产品')
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations', verbose_name='操作人')
    operation_type = models.IntegerField(choices=OPERATION_CHOICES, verbose_name='操作类型')
    description = models.TextField(null=True, blank=True, verbose_name='操作描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        verbose_name = '操作记录'
        verbose_name_plural = '操作记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.qrcode_id} - {self.get_operation_type_display()}"


class RepairRecord(models.Model):
    """维修记录表"""
    STATUS_CHOICES = [
        (1, '待维修'),
        (2, '维修中'),
        (3, '已完成'),
        (4, '无法修复')
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='repair_records', verbose_name='产品')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repair_requests', 
                               limit_choices_to={'user_type': User.ClIENT}, verbose_name='客户')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='repairs_handled',
                                 limit_choices_to={'user_type': User.EMPLOYEE}, verbose_name='技术人员')
    repair_reason = models.TextField(verbose_name='维修原因')
    repair_solution = models.TextField(null=True, blank=True, verbose_name='维修解决方案')
    repair_date = models.DateTimeField(null=True, blank=True, verbose_name='维修日期')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '维修记录'
        verbose_name_plural = '维修记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.qrcode_id} - {self.get_status_display()}"
