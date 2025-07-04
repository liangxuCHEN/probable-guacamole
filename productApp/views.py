from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import authenticate
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404, render

from .models import (
    User, ProductType, Product, OperationRecord, RepairRecord
)
from .serializers import (
    UserSerializer, UserLoginSerializer, ProductTypeSerializer, ProductSerializer,
    ProductCreateSerializer, ProductBulkCreateSerializer, ProductShippingSerializer,
    ProductActivationSerializer, OperationRecordSerializer, RepairRecordSerializer,
    RepairRecordCreateSerializer, WarrantyCheckSerializer
)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductActivationSerializer
from .models import Product, OperationRecord

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([])  # 禁用JWT认证
@permission_classes([AllowAny])
def warranty_registration(request):
    """产品保修登记-表单"""
    if request.method == 'GET':
        return render(request, 'warranty-registration.html')
    
    elif request.method == 'POST':
        try:
            # 处理图片上传和二维码识别
            if 'image' not in request.FILES:
                return JsonResponse({
                    'status': 'error',
                    'message': '请上传图片'
                }, status=400)

            image = request.FILES['image']

            # 使用OpenCV和pyzbar进行二维码识别
            import cv2
            import numpy as np
            import os
            import tempfile
            from pyzbar.pyzbar import decode
            
            # 先保存图片到临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            try:
                # 读取保存的图片
                image_array = cv2.imread(temp_file_path)
                if image_array is None:
                    return JsonResponse({
                        'status': 'error',
                        'message': '图片读取失败，请重新上传'
                    }, status=400)
                
                decoded_objects = decode(image_array)
            finally:
                # 删除临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

            if not decoded_objects:
                return JsonResponse({
                    'status': 'error',
                    'message': '未能识别二维码，请确保图片清晰'
                }, status=400)

            # 获取二维码内容（产品ID）
            qrcode_id = decoded_objects[0].data.decode('utf-8')

            # 查询产品信息
            try:
                product = Product.objects.get(qrcode_id=qrcode_id)
                # 检查产品状态
                if product.status == 3:  # 已激活
                    return JsonResponse({
                        'status': 'success',
                        'message': '产品已激活',
                        'data': {
                            'is_activated': True,
                            'product': {
                                'qrcode_id': product.qrcode_id,
                                'name': product.name,
                                'email': product.email,
                                'activation_date': product.activation_date.strftime('%Y-%m-%d %H:%M:%S') if product.activation_date else None,
                                'warranty_start': product.warranty_start_date.strftime('%Y-%m-%d %H:%M:%S') if product.warranty_start_date else None,
                                'warranty_end': product.warranty_end_date.strftime('%Y-%m-%d %H:%M:%S') if product.warranty_end_date else None,
                                'under_warranty': product.is_under_warranty(),
                                'status': product.get_status_display()
                            }
                        }
                    })
                elif product.status == 2:  # 已出货，可以激活
                    return JsonResponse({
                        'status': 'success',
                        'message': '产品未激活',
                        'data': {
                            'is_activated': False,
                            'product': {
                                'qrcode_id': product.qrcode_id,
                                'product_type': product.product_type.name if product.product_type else None
                            }
                        }
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': '产品状态异常，无法激活'
                    }, status=400)

            except Product.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': '未找到该产品'
                }, status=404)
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'处理失败：{str(e)}'
            }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def activate_product(request):
    """产品激活API"""
    serializer = ProductActivationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            product = get_object_or_404(
                Product,
                qrcode_id=serializer.validated_data['qrcode_id'],
                status=2  # 只能激活状态为"已出货"的产品
            )
            
            # 更新产品的客户信息
            product.name = serializer.validated_data['name']
            product.phone = serializer.validated_data.get('phone')
            product.email = serializer.validated_data.get('email')
            product.city = serializer.validated_data.get('city')
            product.country = serializer.validated_data.get('country')
            
            if product.activate():
                product.save()  # 保存客户信息
                # 创建操作记录
                OperationRecord.objects.create(
                    product=product,
                    operator=f"client-{product.name}",
                    operation_type=3,  # 产品激活
                    description=f"产品被客户 {product.name} 激活"
                )
                return Response({
                    'status': 'success',
                    'message': '产品激活成功',
                    'data': {
                        'qrcode_id': product.qrcode_id,
                        'name': product.name,
                        'email': product.email,
                        'activation_date': product.activation_date.strftime('%Y-%m-%d %H:%M:%S') if product.activation_date else None,
                        'warranty_start': product.warranty_start_date.strftime('%Y-%m-%d %H:%M:%S') if product.warranty_start_date else None,
                        'warranty_end': product.warranty_end_date.strftime('%Y-%m-%d %H:%M:%S') if product.warranty_end_date else None,
                        'under_warranty': product.is_under_warranty(),
                    }
                })
            return Response({
                'status': 'error',
                'message': '产品无法激活'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': '未找到该产品'
            }, status=status.HTTP_404_NOT_FOUND)
    return Response({
        'status': 'error',
        'message': '输入数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录接口"""
    print(request.data)
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)

            return Response({
                'status': 'success',
                'message': '登录成功',
                'data': {
                    'user': user_serializer.data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            })
        else:
            return Response({
                'status': 'error',
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response({
        'status': 'error',
        'message': '输入数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_permissions(self):
        """根据不同的操作设置不同的权限"""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前登录用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProductTypeViewSet(viewsets.ModelViewSet):
    """产品类型管理视图集"""
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'model_number']
    search_fields = ['name', 'model_number', 'description']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """只有管理员可以创建、更新和删除产品类型"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    """产品管理视图集"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['qrcode_id', 'product_type', 'status', 'agent']
    search_fields = ['qrcode_id']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        """根据不同的操作设置不同的权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """创建产品时自动记录操作"""
        product = serializer.save()
        OperationRecord.objects.create(
            product=product,
            operator=f"user-{self.request.user.username}",
            operation_type=1,  # 创建产品
            description=f"创建产品 {product.qrcode_id}"
        )

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """批量创建产品"""
        serializer = ProductBulkCreateSerializer(data=request.data)
        if serializer.is_valid():
            product_type = get_object_or_404(ProductType, id=serializer.validated_data['product_type_id'])
            products = []
            for qrcode_id in serializer.validated_data['qrcode_ids']:
                products.append(Product(
                    qrcode_id=qrcode_id,
                    product_type=product_type
                ))
            
            with transaction.atomic():
                created_products = Product.objects.bulk_create(products)
                # 批量创建操作记录
                operation_records = [
                    OperationRecord(
                        product=product,
                        operator=f"user-{self.request.user.username}",
                        operation_type=1,
                        description=f"批量创建产品 {product.qrcode_id}"
                    ) for product in created_products
                ]
                OperationRecord.objects.bulk_create(operation_records)
            
            return Response({
                'status': 'success',
                'message': f'成功创建 {len(created_products)} 个产品'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_shipping(self, request):
        """批量发货"""
        serializer = ProductShippingSerializer(data=request.data)
        if serializer.is_valid():
            agent = get_object_or_404(User, id=serializer.validated_data['agent_id'], user_type=User.AGENT)
            shipping_date = serializer.validated_data.get('shipping_date', timezone.now())
            
            with transaction.atomic():
                # 更新产品信息
                products = Product.objects.filter(
                    qrcode_id__in=serializer.validated_data['qrcode_ids'],
                    status=1  # 只能发货状态为"已生成"的产品
                )
                if not products.exists():
                    return Response({
                        'status': 'error',
                        'message': '未找到可发货的产品'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                products.update(
                    agent=agent,
                    shipping_date=shipping_date,
                    status=2  # 更新状态为"已出货"
                )
                
                # 创建操作记录
                operation_records = [
                    OperationRecord(
                        product=product,
                        operator=f"user-{self.request.user.username}",
                        operation_type=2,  # 产品出货
                        description=f"产品出货给代理商 {agent.username}"
                    ) for product in products
                ]
                OperationRecord.objects.bulk_create(operation_records)
            
            return Response({
                'status': 'success',
                'message': f'成功发货 {products.count()} 个产品给代理商 {agent.username}'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def activate(self, request):
        """激活产品"""
        serializer = ProductActivationSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(
                Product,
                qrcode_id=serializer.validated_data['qrcode_id'],
                status=2  # 只能激活状态为"已出货"的产品
            )
            
            # 更新产品的客户信息
            product.name = serializer.validated_data['name']
            product.phone = serializer.validated_data['phone']
            product.email = serializer.validated_data.get('email')
            product.city = serializer.validated_data.get('city')
            product.country = serializer.validated_data.get('country')
            
            if product.activate():
                product.save()  # 保存客户信息
                # 创建操作记录
                OperationRecord.objects.create(
                    product=product,
                    operator=f"user-{self.request.user.username}",
                    operation_type=3,  # 产品激活
                    description=f"产品被客户 {product.name} 激活"
                )
                return Response({
                    'status': 'success',
                    'message': '产品激活成功'
                })
            return Response({
                'status': 'error',
                'message': '产品无法激活'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_warranty(self, request):
        """查询保修状态"""
        serializer = WarrantyCheckSerializer(data=request.data)
        if serializer.is_valid():
            filters = {}
            if qrcode_id := serializer.validated_data.get('qrcode_id'):
                filters['qrcode_id'] = qrcode_id
            if customer_email := serializer.validated_data.get('customer_email'):
                filters['email'] = customer_email
            if customer_phone := serializer.validated_data.get('customer_phone'):
                filters['phone'] = customer_phone
            
            products = Product.objects.filter(**filters)
            if not products.exists():
                return Response({
                    'status': 'error',
                    'message': '未找到相关产品'
                }, status=status.HTTP_404_NOT_FOUND)
            
            results = []
            for product in products:
                results.append({
                    'qrcode_id': product.qrcode_id,
                    'product_type': product.product_type.name,
                    'under_warranty': product.is_under_warranty(),
                    'warranty_start': product.warranty_start_date,
                    'warranty_end': product.warranty_end_date,
                    'status': product.get_status_display()
                })
            
            return Response({
                'status': 'success',
                'data': results
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def get_by_qrcode(self, request):
        """通过qrcode_id查询产品信息"""
        qrcode_id = request.query_params.get('qrcode_id')
        if not qrcode_id:
            return Response({
                'status': 'error',
                'message': '请提供qrcode_id参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = get_object_or_404(Product, qrcode_id=qrcode_id)
            serializer = self.get_serializer(product)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': '未找到该产品'
            }, status=status.HTTP_404_NOT_FOUND)


class OperationRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """操作记录视图集 - 只读"""
    queryset = OperationRecord.objects.all()
    serializer_class = OperationRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'operator', 'operation_type']
    search_fields = ['product__qrcode_id', 'description']
    permission_classes = [IsAuthenticated]


class RepairRecordViewSet(viewsets.ModelViewSet):
    """维修记录管理视图集"""
    queryset = RepairRecord.objects.all()
    serializer_class = RepairRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'customer', 'technician', 'status']
    search_fields = ['product__qrcode_id', 'repair_reason', 'repair_solution']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RepairRecordCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """创建维修记录时自动更新产品状态并创建操作记录"""
        try:
            with transaction.atomic():
                repair_record = serializer.save()
                product = repair_record.product
                
                # 更新产品状态为维修中
                product.status = 4  # 维修中
                product.save()
                
                # 创建操作记录
                OperationRecord.objects.create(
                    product=product,
                    operator=f"user-{self.request.user.username}",
                    operation_type=4,  # 维修登记
                    description=f"客户 {product.name} 的产品进入维修，原因：{repair_record.repair_reason}"
                )
        except Exception as e:
            raise ValidationError(f"创建维修记录失败：{str(e)}")

    @action(detail=True, methods=['post'])
    def complete_repair(self, request, pk=None):
        """完成维修"""
        repair_record = self.get_object()
        if repair_record.status != 2:  # 只有状态为"维修中"的记录才能标记为完成
            return Response({
                'status': 'error',
                'message': '只有正在维修中的记录才能标记为完成'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            repair_record.status = 3  # 已完成
            repair_record.repair_date = timezone.now()
            repair_record.save()
            
            # 更新产品状态为已激活
            product = repair_record.product
            product.status = 3  # 已激活
            product.save()
            
            # 创建操作记录
            OperationRecord.objects.create(
                product=product,
                operator=f"user-{self.request.user.username}",
                operation_type=5,  # 维修完成
                description=f"产品维修完成，解决方案：{repair_record.repair_solution}"
            )
        
        return Response({
            'status': 'success',
            'message': '维修完成'
        })