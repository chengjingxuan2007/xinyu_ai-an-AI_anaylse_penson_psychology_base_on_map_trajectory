from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile


def _generate_token(user):
    """生成JWT Token并返回"""
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
        'nickname': user.nickname or user.username,
    }


def _validate_registration(username, password, confirm_password):
    """校验注册参数合法性（含 Django 密码强度校验器）"""
    if not username or not password:
        return False, "用户名和密码不能为空"
    if password != confirm_password:
        return False, "两次密码输入不一致"
    if UserProfile.objects.filter(username=username).exists():
        return False, "用户名已存在"
    try:
        validate_password(password)  # 触发 settings 里的强度规则（长度≥8等）
    except ValidationError as e:
        return False, e.messages[0]
    return True, ""


class RegisterView(APIView):
    """用户注册接口 POST /api/user/register/"""

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')
        nickname = request.data.get('nickname', '').strip()

        is_valid, error_msg = _validate_registration(username, password, confirm_password)
        if not is_valid:
            return Response({'code': 400, 'msg': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.create_user(
            username=username,
            password=password,
            nickname=nickname
        )
        token_data = _generate_token(user)
        return Response({'code': 200, 'msg': '注册成功', 'data': token_data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """用户登录接口 POST /api/user/login/"""

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response({'code': 400, 'msg': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'code': 401, 'msg': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        token_data = _generate_token(user)
        return Response({'code': 200, 'msg': '登录成功', 'data': token_data})