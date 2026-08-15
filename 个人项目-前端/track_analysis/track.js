const API_BASE = 'http://127.0.0.1:8000/api';
// 模拟出行时长：1.5 小时（demo 数据，后续可接真实记录）
const TRACK_MINUTES = 90;

// 两点间距离（米），Haversine 公式
function segDist(a, b) {
    const R = 6371000, rad = x => x * Math.PI / 180;
    const dLat = rad(b[1] - a[1]), dLon = rad(b[0] - a[0]);
    const s = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a[1])) * Math.cos(rad(b[1])) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(s));
}

// 地图画好后（map.js 先注册，先执行），统计时间/距离/速度
document.addEventListener("DOMContentLoaded", function () {
    const coords = window.trackCoords || [];
    let meters = 0;
    for (let i = 1; i < coords.length; i++) meters += segDist(coords[i - 1], coords[i]);

    const km = meters / 1000;
    const hours = TRACK_MINUTES / 60;
    document.getElementById('stat-time').innerText = '1 小时 30 分';
    document.getElementById('stat-dist').innerText = km.toFixed(2) + ' km';
    document.getElementById('stat-speed').innerText = (km / hours).toFixed(1) + ' km/h';
});

// 调后端 AI 接口，根据轨迹统计做情绪分析
async function analyzeTrack() {
    const output = document.getElementById('track-output');
    const token = localStorage.getItem('access_token');
    if (!token) { output.innerText = '请先登录后再使用轨迹分析'; return; }

    const dist = document.getElementById('stat-dist').innerText;
    const speed = document.getElementById('stat-speed').innerText;
    const message = `我今天的轨迹：总距离${dist}，出行时间1小时30分，平均速度${speed}，共经过${(window.trackCoords || []).length}个位置点。请结合这些数据，分析我今天可能的情绪状态，并给我一些温暖的建议。`;

    output.innerText = 'AI 正在分析你的轨迹，请稍候...';
    try {
        const res = await fetch(`${API_BASE}/ai_app/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ message, session_id: null, mode: 'normal' })
        });
        const data = await res.json();
        if (res.ok && data.code === 200) {
            output.innerText = data.data.reply;
        } else if (res.status === 401) {
            output.innerText = '登录已过期，请重新登录';
        } else {
            output.innerText = data.msg || '出错了，请稍后再试';
        }
    } catch (err) {
        output.innerText = '网络异常，请检查后端服务是否启动';
    }
}
