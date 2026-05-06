# 天气查看应用 🌤️

一个简洁美观的天气查看 Web 应用，支持查询全球城市的实时天气和 7 天预报。

## 功能特点

- 🌍 支持全球城市搜索（中文、英文城市名均可）
- 🌡️ 显示实时温度、体感温度、湿度、风速
- 📅 7 天天气预报
- 💧 降水概率显示
- 📱 响应式设计，支持移动端
- 🆓 使用免费的 Open-Meteo API，无需 API Key

## 快速开始

### 1. 安装依赖

```bash
cd weather_app
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

## 使用方法

1. 在搜索框中输入城市名称（如：北京、上海、Tokyo、New York）
2. 点击"查询"按钮或按回车键
3. 查看当前天气和 7 天预报

## 技术栈

- **后端**: Python Flask
- **前端**: HTML5, CSS3, JavaScript (原生)
- **天气 API**: [Open-Meteo](https://open-meteo.com/) (免费开源)
- **地理编码**: Open-Meteo Geocoding API

## 项目结构

```
weather_app/
├── app.py              # Flask 后端应用
├── requirements.txt    # Python 依赖
├── README.md          # 项目说明
├── templates/
│   └── index.html     # 前端页面模板
└── static/
    ├── style.css      # 样式文件
    └── script.js      # 前端脚本
```

## API 接口

### GET /api/weather

查询天气数据。

**参数**:
- `city`: 城市名称（必填）

**响应示例**:

```json
{
  "location": {
    "name": "北京",
    "country": "中国",
    "admin1": "北京",
    "latitude": 39.9075,
    "longitude": 116.39723
  },
  "current": {
    "temperature": 25,
    "feels_like": 26,
    "humidity": 45,
    "wind_speed": 12,
    "description": "晴朗",
    "icon": "☀️"
  },
  "forecast": [...]
}
```

## 许可证

MIT License
