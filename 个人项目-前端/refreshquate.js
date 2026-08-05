// 定义句子库（确保在函数外部或顶部定义，以便全局访问）
const comfortQuotes = [
    "“你不需要时刻都坚强，允许自己脆弱，也是一种勇敢。”",
    "“生活不是等待暴风雨过去，而是学会在雨中翩翩起舞。”",
    "“每一个不起舞的日子，都是对生命的辜负。今天也要加油哦！”",
    "“无论今晚多么黑暗，明天太阳依旧升起。希望就在前方。”",
    "“深呼吸，吸气——呼气——一切都会好起来的。”"
];

function refreshQuote() {
    // 1. 获取DOM元素
    const quoteElement = document.getElementById('daily-quote');
    
    // 2. 安全检查：防止元素不存在导致报错
    if (!quoteElement) return;

    // 3. 执行淡出动画
    quoteElement.style.opacity = 0;

    // 4. 延迟更换文字并淡入
    setTimeout(() => {
        // 随机选择一句
        const randomIndex = Math.floor(Math.random() * comfortQuotes.length);
        quoteElement.innerText = comfortQuotes[randomIndex];
        
        // 恢复透明度
        quoteElement.style.opacity = 1;
    }, 300); // 300ms 与 CSS transition 时间保持一致
}