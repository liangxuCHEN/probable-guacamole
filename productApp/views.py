from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import authenticate
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import User
from .serializers import UserSerializer, UserLoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录接口"""
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