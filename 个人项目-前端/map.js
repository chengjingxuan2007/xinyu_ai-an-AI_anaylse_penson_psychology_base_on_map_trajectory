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
                    zoom: 14, // 初始缩放级别稍微调小一点，以便看到全貌，你可以按需调整
                    minZoom: 3,  // 最小缩放级别，防止缩得太小没有瓦片
                    maxZoom: 18  // 最大缩放级别，高德瓦片最多支持到18
                })
    });

    // 将map对象挂载到window上，方便在其他脚本中调用地图实例（例如添加轨迹点）
    window.myMapInstance = map;

    // ===== 轨迹绘制（demo 数据写死，必须等地图创建完成后再执行）=====

    // ① 轨迹数据：写死一串经纬度坐标（经度, 纬度），模拟"今天走过的路"
    const trackCoords = [
        [106.96, 33.21],   // 起点
        [106.965, 33.215],
        [106.97, 33.212],
        [106.975, 33.22],
        [106.982, 33.218],
        [106.988, 33.225]  // 终点
    ];
    // 暴露轨迹坐标，供轨迹分析页统计使用
    window.trackCoords = trackCoords;

    // ② 把经纬度转成 OpenLayers 内部坐标，然后画成一条线
    const trackLine = new ol.Feature({
        geometry: new ol.geom.LineString(
            trackCoords.map(coord => ol.proj.fromLonLat(coord))  // 逐个转换
        )
    });
    trackLine.setStyle(new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#11998e',   // 线的颜色（和你页面主题一致）
            width: 2           // 线宽
        })
    }));

    // ③ 起点和终点各放一个圆点标记
    function makePoint(coord, color) {
        const p = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat(coord))
        });
        p.setStyle(new ol.style.Style({
            image: new ol.style.Circle({
                radius: 6,
                fill: new ol.style.Fill({ color: color })
            })
        }));
        return p;
    }
    const startPoint = makePoint(trackCoords[0], '#e8463a');                      // 起点红色
    const endPoint   = makePoint(trackCoords[trackCoords.length - 1], '#38ef7d'); // 终点绿色

    // ④ 把线 + 两个点装进矢量图层，加到地图上
    const trackLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [trackLine, startPoint, endPoint]
        })
    });
    map.addLayer(trackLayer);

    // ⑤ 自动缩放视野，让整条轨迹刚好完整显示
    map.getView().fit(
        trackLine.getGeometry().getExtent(),   // 线的范围
        { padding: [80, 80, 80, 80], duration: 500 }  // 四周留白，动画过渡
    );
});