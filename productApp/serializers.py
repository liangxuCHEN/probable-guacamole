from rest_framework import serializers
from .models import User, WechatProfile, ProductType, Product, OperationRecord, RepairRecord


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
    customer_name = serializers.ReadOnlyField(source='customer.username', allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    under_warranty = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'qrcode_id', 'product_type', 'product_type_name', 'agent', 'agent_name', 
                 'shipping_date', 'activation_date', 'customer', 'customer_name', 
                 'warranty_start_date', 'warranty_end_date', 'status', 'status_display', 
                 'under_warranty', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'warranty_start_date', 'warranty_end_date']
    
    def get_under_warranty(self, obj):
        return obj.is_under_warranty()


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['qrcode_id', 'product_type']


class ProductBulkCreateSerializer(serializers.Serializer):
    product_type_id = serializers.IntegerField()
    qrcode_ids = serializers.ListField(child=serializers.CharField(max_length=100))


class ProductShippingSerializer(serializers.Serializer):
    qrcode_ids = serializers.ListField(child=serializers.CharField(max_length=100))
    agent_id = serializers.IntegerField()
    shipping_date = serializers.DateTimeField(required=False)


class ProductActivationSerializer(serializers.Serializer):
    qrcode_id = serializers.CharField(max_length=100)
    customer_id = serializers.IntegerField()


class OperationRecordSerializer(serializers.ModelSerializer):
    product_qrcode = serializers.ReadOnlyField(source='product.qrcode_id')
    operator_name = serializers.ReadOnlyField(source='operator.username')
    operation_type_display = serializers.CharField(source='get_operation_type_display', read_only=True)
    
    class Meta:
        model = OperationRecord
        fields = ['id', 'product', 'product_qrcode', 'operator', 'operator_name', 
                 'operation_type', 'operation_type_display', 'description', 'created_at']
        read_only_fields = ['created_at']


class RepairRecordSerializer(serializers.ModelSerializer):
    product_qrcode = serializers.ReadOnlyField(source='product.qrcode_id')
    customer_name = serializers.ReadOnlyField(source='customer.username')
    technician_name = serializers.ReadOnlyField(source='technician.username', allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = RepairRecord
        fields = ['id', 'product', 'product_qrcode', 'customer', 'customer_name', 
                 'technician', 'technician_name', 'repair_reason', 'repair_solution', 
                 'repair_date', 'status', 'status_display', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RepairRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRecord
        fields = ['product', 'customer', 'repair_reason']


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