from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

# 创建路由器
router = DefaultRouter()
app_name = 'productApp'

# 注册视图集
router.register(r'users', views.UserViewSet)
router.register(r'product-types', views.ProductTypeViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'operation-records', views.OperationRecordViewSet)
router.register(r'repair-records', views.RepairRecordViewSet)
router.register(r'attachments', views.AttachmentViewSet)


urlpatterns = [
    # JWT 相关接口
    path('auth/login/', views.login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('wr', views.warranty_registration, name='warranty'),
    path('wr_api', views.warranty_registration_api, name='warranty_api'),
    path('code_api', views.check_code_api, name='check_code_api'),
    path('activate-product/', views.activate_product, name='activate_product'),
    # API 路由
    path('', include(router.urls)),
]