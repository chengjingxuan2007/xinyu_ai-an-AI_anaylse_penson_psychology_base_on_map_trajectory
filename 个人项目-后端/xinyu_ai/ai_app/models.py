from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    """AI 咨询会话：一个用户可开启多个会话，用于多轮对话记忆"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_sessions',
        verbose_name='用户',
    )
    title = models.CharField(max_length=50, blank=True, default='', verbose_name='会话标题')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后活跃时间')

    class Meta:
        db_table = 'ai_chat_session'
        ordering = ['-updated_at']
        verbose_name = 'AI 咨询会话'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} - {self.title or self.id}'


class ChatMessage(models.Model):
    """会话中的单条消息（用户 / AI 回复）"""
    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', 'AI'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='所属会话',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        db_table = 'ai_chat_message'
        ordering = ['created_at', 'id']
        verbose_name = '对话消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.role}: {self.content[:20]}'
