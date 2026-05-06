"""
天气查看应用 - 后端 API
使用 Flask 和 Open-Meteo API（免费、无需 API key）
"""

import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: ("晴朗", "☀️"),
    1: ("大部晴朗", "🌤️"),
    2: ("部分多云", "⛅"),
    3: ("多云", "☁️"),
    45: ("雾", "🌫️"),
    48: ("雾凇", "🌫️"),
    51: ("小毛毛雨", "🌧️"),
    53: ("中毛毛雨", "🌧️"),
    55: ("大毛毛雨", "🌧️"),
    56: ("冻毛毛雨", "🌧️"),
    57: ("冻毛毛雨", "🌧️"),
    61: ("小雨", "🌧️"),
    63: ("中雨", "🌧️"),
    65: ("大雨", "🌧️"),
    66: ("冻雨", "🌧️"),
    67: ("冻雨", "🌧️"),
    71: ("小雪", "🌨️"),
    73: ("中雪", "🌨️"),
    75: ("大雪", "🌨️"),
    77: ("雪粒", "🌨️"),
    80: ("小阵雨", "🌦️"),
    81: ("中阵雨", "🌦️"),
    82: ("大阵雨", "🌦️"),
    85: ("小阵雪", "🌨️"),
    86: ("大阵雪", "🌨️"),
    95: ("雷暴", "⛈️"),
    96: ("雷暴伴小冰雹", "⛈️"),
    99: ("雷暴伴大冰雹", "⛈️"),
}


def get_weather_description(code: int) -> tuple[str, str]:
    """根据天气代码获取描述和图标"""
    return WEATHER_CODES.get(code, ("未知", "❓"))


def search_location(query: str) -> dict | None:
    """搜索地点获取经纬度"""
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": query, "count": 1, "language": "zh"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "name": result.get("name", query),
                "country": result.get("country", ""),
                "admin1": result.get("admin1", ""),
                "latitude": result["latitude"],
                "longitude": result["longitude"],
            }
        return None
    except requests.RequestException:
        return None


def get_weather(latitude: float, longitude: float) -> dict | None:
    """获取天气数据"""
    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset",
                "timezone": "auto",
                "forecast_days": 7,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


@app.route("/")
def index():
    """首页"""
    return render_template("index.html")


@app.route("/api/weather")
def api_weather():
    """天气 API 接口"""
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "请输入城市名称"}), 400

    location = search_location(city)
    if not location:
        return jsonify({"error": f"未找到城市: {city}"}), 404

    weather_data = get_weather(location["latitude"], location["longitude"])
    if not weather_data:
        return jsonify({"error": "获取天气数据失败"}), 500

    current = weather_data.get("current", {})
    daily = weather_data.get("daily", {})

    weather_code = current.get("weather_code", 0)
    description, icon = get_weather_description(weather_code)

    forecast = []
    if daily:
        times = daily.get("time", [])
        codes = daily.get("weather_code", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        precip_probs = daily.get("precipitation_probability_max", [])
        sunrises = daily.get("sunrise", [])
        sunsets = daily.get("sunset", [])

        for i in range(len(times)):
            day_desc, day_icon = get_weather_description(codes[i] if i < len(codes) else 0)
            forecast.append({
                "date": times[i] if i < len(times) else "",
                "description": day_desc,
                "icon": day_icon,
                "temp_max": max_temps[i] if i < len(max_temps) else None,
                "temp_min": min_temps[i] if i < len(min_temps) else None,
                "precipitation_probability": precip_probs[i] if i < len(precip_probs) else None,
                "sunrise": sunrises[i].split("T")[1] if i < len(sunrises) else "",
                "sunset": sunsets[i].split("T")[1] if i < len(sunsets) else "",
            })

    result = {
        "location": {
            "name": location["name"],
            "country": location["country"],
            "admin1": location["admin1"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "current": {
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "wind_direction": current.get("wind_direction_10m"),
            "weather_code": weather_code,
            "description": description,
            "icon": icon,
        },
        "forecast": forecast,
        "timezone": weather_data.get("timezone", ""),
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
