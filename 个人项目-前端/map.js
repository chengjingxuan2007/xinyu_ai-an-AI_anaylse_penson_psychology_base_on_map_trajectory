document.addEventListener("DOMContentLoaded", function () {
    // 检查页面上是否存在id为'map'的元素
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.warn("未找到ID为'map'的容器，地图未初始化。");
        return;
    }

    // 初始化地图
    const map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.XYZ({
                    // 高德地图矢量图层（国内访问速度快，风格简洁）
                    url: 'https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}'
                })
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([106.96, 33.21]), //汉中市位置
            zoom: 14 // 初始缩放级别稍微调小一点，以便看到全貌，你可以按需调整
        })
    });

    // 将map对象挂载到window上，方便在其他脚本中调用地图实例（例如添加轨迹点）
    window.myMapInstance = map;
});