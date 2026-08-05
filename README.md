# 心语AI - 基于地图轨迹的心理分析平台

> 个人国创项目（大创训练计划）· 概念验证原型

一个以 **Python Web 全栈** 为基础、以 **GIS 轨迹跟踪** 为核心卖点的心理分析平台原型。用户可通过 AI 心理咨询对话获得情绪陪伴，项目规划通过地图轨迹数据（活动范围、停留热点）结合情绪日记做行为层面的心理分析。

---

## 项目结构

```
├── 个人项目-前端/            # 原生 HTML/CSS/JS 前端
│   ├── index.html            # 登录页
│   ├── register.html         # 注册页
│   ├── main.html             # 主页面（AI 咨询 + 地图 + 日记入口）
│   ├── map.js                # OpenLayers 地图（高德底图）
│   └── mood_diary/           # 心情日记页
└── 个人项目-后端/            # Django REST Framework 后端
    └── xinyu_ai/
        ├── xinyu_ai/         # 项目配置（settings / urls）
        ├── user_app/         # 用户注册 / 登录（JWT 认证）
        ├── ai_app/           # AI 心理咨询（DeepSeek 接入）
        ├── map_app/          # 地图轨迹（规划中）
        └── mood_diary/       # 心情日记（规划中）
```

---

## 技术栈

| 层次 | 技术 | 用途 |
|---|---|---|
| 后端框架 | Django 5.2 + Django REST Framework | API 服务 |
| 认证 | JWT（simplejwt） | 无状态登录认证 |
| 数据库 | MySQL（PyMySQL 驱动） | 用户 / 会话 / 消息存储 |
| AI 能力 | DeepSeek API（OpenAI 兼容） | 心理陪伴对话 |
| 前端 | 原生 HTML/CSS/JS + Fetch | 前后端分离交互 |
| GIS | OpenLayers + 高德底图 | 地图可视化（轨迹规划中） |

---

## 已实现功能

- ✅ 用户注册 / 登录（JWT 无状态认证，Token 存前端 localStorage）
- ✅ AI 心理咨询对话
  - 多轮记忆（session_id 关联会话，历史消息回传大模型）
  - 医学红线拦截（关键词过滤 + 系统提示词双重防护，不提供诊断/用药建议）
  - 请求长度限制与上下文截断（防刷与成本控制）
- ✅ 接口安全
  - 医学咨询关键词过滤
  - DRF 全局节流（防暴力破解 / 防 API 刷费）
  - 密码强度校验（Django validate_password）
  - 密钥外置（.env 环境变量，不进 git）
- ✅ 地图底图展示（OpenLayers + 高德瓦片，汉中市默认视图）

## 规划中功能

- [ ] 用户 GPS 轨迹采集（浏览器 Geolocation API）
- [ ] 轨迹存储与可视化（MySQL 存点，OpenLayers 画线）
- [ ] 轨迹情绪关联分析（活动范围 / 停留热点 → AI 行为分析）
- [ ] 心情日记完整 CRUD 与情绪曲线

---

## 本地运行

```bash
# 1. 后端
cd 个人项目-后端/xinyu_ai
pip install -r requirements.txt
cp .env.example .env      # 填入 SECRET_KEY / DB_PASSWORD / DEEPSEEK_API_KEY
python manage.py migrate
python manage.py runserver

# 2. 前端（静态服务器，如 VS Code Live Server）
# 打开 个人项目-前端/index.html，端口需为 5500（CORS 白名单）
```

> 前端通过 `http://127.0.0.1:8000/api` 与后端交互，CORS 白名单仅放行 `http://127.0.0.1:5500`。
> 浏览器定位功能在正式部署时需 HTTPS 环境。

---

## 项目状态

当前为**概念验证（MVP）阶段**：核心链路（登录 → AI 对话 → 多轮记忆 → 安全红线）已跑通；GIS 轨迹采集与分析为下一阶段重点。
