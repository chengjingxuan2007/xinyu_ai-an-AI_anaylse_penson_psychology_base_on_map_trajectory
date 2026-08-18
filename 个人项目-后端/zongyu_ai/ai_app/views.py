from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatMessage, ChatSession
from .prompt import MAX_INPUT_LENGTH, call_ai_api, is_medical_query, medical_refusal,MODE_PROMPTS


class ChatView(APIView):
    """AI 咨询对话接口：POST /api/ai_app/chat/

    请求体：
      message     用户说的话（必填）
      session_id  会话 ID（第一次对话可以不带，之后带上才能多轮记忆）
    返回：
      data.reply       AI 的回复
      data.session_id  本次会话 ID（前端保存好，下次对话再传回来）
    """

    # 要求登录：前端请求时要在请求头带上 JWT Token（Authorization: Bearer <token>）
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. 拿到用户说的话和会话 ID
        message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id')
        mode = request.data.get('mode', 'normal')
        if mode not in MODE_PROMPTS:
            mode = 'normal'  # 不认识的模式一律回退到普通

        # 2. 校验：不能为空、不能太长
        if not message:
            return Response({'code': 400, 'msg': '请输入咨询内容哦'}, status=status.HTTP_400_BAD_REQUEST)
        if len(message) > MAX_INPUT_LENGTH:
            return Response(
                {'code': 400, 'msg': f'内容太长了，请控制在 {MAX_INPUT_LENGTH} 字以内'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. 找到或新建会话：传了 session_id 且属于当前用户就接着聊，否则开新会话
        session = ChatSession.objects.filter(id=session_id, user=request.user).first() if session_id else None
        if session is None:
            session = ChatSession.objects.create(user=request.user)

        # 4. 医学红线：涉及诊断/用药/治疗的问题，不调用大模型，直接礼貌回避
        if is_medical_query(message):
            reply = medical_refusal()
        else:
            # 5. 把历史对话整理成列表，和当前消息一起发给 AI，它才能记住上下文
            history = [
                {'role': msg.role, 'content': msg.content}
                for msg in session.messages.all()
            ]
            reply = call_ai_api(message, history,mode)

        # 6. 把「用户消息 + AI 回复」存进数据库，下一轮对话要用
        if not session.messages.exists():
            # 第一次对话，用这句话当会话标题（方便以后查看历史）
            session.title = message[:20]
            session.save()
        ChatMessage.objects.create(session=session, role='user', content=message)
        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        # 7. 把结果返回给前端（session_id 也要返回，前端下次对话要用）
        return Response(
            {'code': 200, 'msg': 'success', 'data': {'reply': reply, 'session_id': session.id}},
            status=status.HTTP_200_OK,
        )
