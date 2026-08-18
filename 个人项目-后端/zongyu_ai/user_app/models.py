from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """
    自定义用户模型
    继承AbstractUser已包含: username, password, email, is_active等字段
    """
    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    avatar = models.URLField(blank=True, verbose_name="头像URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta:
        db_table = "user_profile"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
