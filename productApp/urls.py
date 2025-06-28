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


urlpatterns = [
    # JWT 相关接口
    path('auth/login/', views.login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # API 路由
    path('', include(router.urls)),
]