"""ai_app/prompt.py
AI 提示词模板 与 大模型调用接口


"""

import requests
from django.conf import settings

# 系统提示词：定义 AI 的角色、职责与红线
SYSTEM_PROMPT = (
    "你是「心语」，一位知心的心理陪伴同伴，专注于倾听与情绪支持。\n"
    "【你的职责】\n"
    "1. 真诚倾听用户的烦恼，给予共情与温暖。\n"
    "2. 用温和、简洁的语言陪伴用户，帮助缓解情绪。\n"
    "【最高级别指令（不可违反）！！！】\n"
    "1. 绝不给出任何医学上的诊断或建议。\n"
    "2. 绝不建议任何药物、治疗方案。\n"
    "3. 当用户询问诊断、用药、治疗等医学问题时，礼貌回避，"
    "并提醒用户这类问题需要咨询专业医生。\n"
)

# 单次输入长度上限（字符），防止超长内容刷爆上下文
MAX_INPUT_LENGTH = 300

# 每轮最多携带的历史消息条数（超出截断，控制上下文长度与成本）
MAX_HISTORY_MESSAGES = 15

# 医学红线关键词：命中即礼貌回避，不调用大模型
MEDICAL_KEYWORDS = (
    "诊断", "用药", "药物", "药", "治疗",
    "处方", "吃药", "服药", "安眠药", "抑郁症", "焦虑症",'大概是什么问题'
)


def is_medical_query(text: str) -> bool:
    """判断是否触及医学红线（诊断 / 用药 / 治疗等）"""
    return any(word in text for word in MEDICAL_KEYWORDS)


def medical_refusal() -> str:
    """医学问题的礼貌回避话术"""
    return (
        "我没办法对你的情况做出医学判断，这类问题需要专业医生来解答。"
        "但我可以一直陪着你，把心里的难受慢慢说给我听好吗？"
    )


def build_messages(user_message: str, history: list | None = None) -> list:
    """组装发给大模型的消息列表：系统提示词 + 最近历史 + 当前输入"""
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    if history:
        messages.extend(history[-MAX_HISTORY_MESSAGES:])
    messages.append({'role': 'user', 'content': user_message})
    return messages


def call_ai_api(user_message: str, history: list | None = None) -> str:
    """调用 DeepSeek 大模型，返回 AI 回复文本。"""




    # 1. 组装消息：系统提示词 + 最近历史 + 当前咨询
    messages = build_messages(user_message, history)

    # 2. 请求 DeepSeek（OpenAI 兼容接口）
    try:
        response = requests.post(
            url=f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                'Authorization': f"Bearer {settings.DEEPSEEK_API_KEY}",
                'Content-Type': 'application/json',
            },
            json={
                'model': settings.DEEPSEEK_MODEL,
                'messages': messages,
                'temperature': 0.7,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except (requests.RequestException, KeyError, ValueError):
        # 调用失败时给前端一个友好提示，不暴露内部细节
        return "抱歉，我暂时没能收到回复，请稍后再试试。"


