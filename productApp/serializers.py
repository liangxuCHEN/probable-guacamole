from rest_framework import serializers
from .models import User, WechatProfile, ProductType, Product, OperationRecord, RepairRecord, Attachment
from django.contrib.contenttypes.models import ContentType


class WechatProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WechatProfile
        fields = ['id', 'wx_openid', 'wx_unionid', 'wx_nickname', 'wx_avatar', 'created_at']
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    wechat_profile = WechatProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'user_type', 'wechat_profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'model_number', 'specifications', 'description', 'warranty_period', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    product_type_name = serializers.ReadOnlyField(source='product_type.name')
    agent_name = serializers.ReadOnlyField(source='agent.username', allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    under_warranty = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'qrcode_id', 'product_type', 'product_type_name', 'agent', 'agent_name', 
                 'shipping_date', 'activation_date', 'name', 'phone', 'email', 'city', 'country',
                 'warranty_start_date', 'warranty_end_date', 'status', 'status_display', 
                 'under_warranty', 'created_at', 'updated_at', 'factory_remark', 'installer']
        read_only_fields = ['created_at', 'updated_at', 'warranty_start_date', 'warranty_end_date']
    
    def get_under_warranty(self, obj):
        return obj.is_under_warranty()


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['qrcode_id', 'product_type']


class ProductBulkCreateSerializer(serializers.Serializer):
    product_type_id = serializers.IntegerField()
    remark = serializers.CharField(max_length=255, required=False, allow_blank=True)
    qrcode_ids = serializers.ListField(child=serializers.CharField(max_length=100))


class ProductShippingSerializer(serializers.Serializer):
    qrcode_ids = serializers.ListField(child=serializers.CharField(max_length=100))
    agent_id = serializers.IntegerField()
    shipping_date = serializers.DateTimeField(required=False)


class ProductActivationSerializer(serializers.Serializer):
    qrcode_id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    city = serializers.CharField(max_length=50, required=False, allow_blank=True)
    country = serializers.CharField(max_length=50, required=False, allow_blank=True)
    installer = serializers.CharField(max_length=255)

    def validate(self, data):
        """
        验证至少提供了姓名和安装人员信息
        """
        if not data.get('name') or not data.get('installer'):
            raise serializers.ValidationError("客户姓名和安装人员是必填项")
        return data
    

class OperationRecordSerializer(serializers.ModelSerializer):
    product_qrcode = serializers.ReadOnlyField(source='product.qrcode_id')
    operation_type_display = serializers.CharField(source='get_operation_type_display', read_only=True)
    
    class Meta:
        model = OperationRecord
        fields = ['id', 'product', 'product_qrcode', 'operator', 'operator',
                 'operation_type', 'operation_type_display', 'description', 'created_at']
        read_only_fields = ['created_at']


class AttachmentSerializer(serializers.ModelSerializer):
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    
    class Meta:
        model = Attachment
        fields = ['id', 'name', 'file_url', 'file_type', 'file_type_display', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AttachmentCreateSerializer(serializers.ModelSerializer):
    content_type_id = serializers.IntegerField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Attachment
        fields = ['name', 'file_url', 'file_type', 'description', 'content_type_id', 'object_id']
    
    def validate(self, data):
        """
        验证content_type_id和object_id是否有效
        """
        content_type_id = data.get('content_type_id')
        object_id = data.get('object_id')
        
        try:
            content_type = ContentType.objects.get(id=content_type_id)
            model_class = content_type.model_class()
            model_class.objects.get(id=object_id)
        except (ContentType.DoesNotExist, model_class.DoesNotExist):
            raise serializers.ValidationError("提供的内容类型或对象ID无效")
        
        return data


class RepairRecordSerializer(serializers.ModelSerializer):
    product_qrcode = serializers.ReadOnlyField(source='product.qrcode_id')
    technician_name = serializers.ReadOnlyField(source='technician.username', allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = RepairRecord
        fields = ['id', 'product', 'product_qrcode', 'name', 'phone', 'email', 'address', 'country',
                 'technician', 'technician_name', 'repair_reason', 'repair_solution', 
                 'repair_date', 'status', 'status_display', 'attachments', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RepairRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRecord
        fields = ['product', 'repair_reason', 'name', 'phone', 'email', 'address', 'country']
    
    def create(self, validated_data):
        """
        创建维修记录时，从产品中获取客户信息（如果未提供）
        """
        product = validated_data['product']
        
        # 如果未提供客户信息，则从产品中获取
        if not validated_data.get('name'):
            validated_data['name'] = product.name
        if not validated_data.get('phone'):
            validated_data['phone'] = product.phone
        if not validated_data.get('email'):
            validated_data['email'] = product.email
        if not validated_data.get('country'):
            validated_data['country'] = product.country
        
        # 创建维修记录
        repair_record = RepairRecord.objects.create(**validated_data)
        return repair_record


class WarrantyCheckSerializer(serializers.Serializer):
    qrcode_id = serializers.CharField(max_length=100, required=False)
    customer_email = serializers.EmailField(required=False)
    customer_phone = serializers.CharField(max_length=20, required=False)
    
    def validate(self, data):
        """
        检查至少提供了一个查询参数
        """
        if not any(data.values()):
            raise serializers.ValidationError("至少需要提供二维码ID、客户邮箱或电话中的一个")
        return data