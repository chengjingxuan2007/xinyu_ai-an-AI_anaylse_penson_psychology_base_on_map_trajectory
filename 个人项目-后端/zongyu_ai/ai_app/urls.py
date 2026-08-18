from django.urls import path
from .views import ChatView

urlpatterns = [
    # AI 咨询对话：POST /api/ai_app/chat/
    path('chat/', ChatView.as_view(), name='ai-chat'),
]
