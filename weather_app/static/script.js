document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('city-input');
    const searchBtn = document.getElementById('search-btn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const weatherResult = document.getElementById('weather-result');

    function showLoading() {
        loading.classList.remove('hidden');
        error.classList.add('hidden');
        weatherResult.classList.add('hidden');
    }

    function hideLoading() {
        loading.classList.add('hidden');
    }

    function showError(message) {
        hideLoading();
        error.textContent = message;
        error.classList.remove('hidden');
        weatherResult.classList.add('hidden');
    }

    function formatDate(dateStr) {
        const date = new Date(dateStr);
        const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const weekday = weekdays[date.getDay()];

        const today = new Date();
        if (date.toDateString() === today.toDateString()) {
            return '今天';
        }

        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        if (date.toDateString() === tomorrow.toDateString()) {
            return '明天';
        }

        return `${month}/${day} ${weekday}`;
    }

    function displayWeather(data) {
        hideLoading();
        error.classList.add('hidden');

        const location = data.location;
        const current = data.current;
        const forecast = data.forecast;

        document.getElementById('location-name').textContent = location.name;

        let detail = '';
        if (location.admin1) detail += location.admin1;
        if (location.country) detail += (detail ? ', ' : '') + location.country;
        document.getElementById('location-detail').textContent = detail;

        document.getElementById('weather-icon').textContent = current.icon;
        document.getElementById('current-temp').textContent = Math.round(current.temperature);
        document.getElementById('weather-desc').textContent = current.description;
        document.getElementById('feels-like').textContent = `${Math.round(current.feels_like)}°C`;
        document.getElementById('humidity').textContent = `${current.humidity}%`;
        document.getElementById('wind-speed').textContent = `${current.wind_speed} km/h`;

        const forecastList = document.getElementById('forecast-list');
        forecastList.innerHTML = '';

        forecast.forEach(day => {
            const item = document.createElement('div');
            item.className = 'forecast-item';

            let precipHtml = '';
            if (day.precipitation_probability !== null && day.precipitation_probability > 0) {
                precipHtml = `<div class="precip">💧 ${day.precipitation_probability}%</div>`;
            }

            item.innerHTML = `
                <div class="date">${formatDate(day.date)}</div>
                <div class="icon">${day.icon}</div>
                <div class="temps">
                    <span class="temp-max">${Math.round(day.temp_max)}°</span>
                    <span class="temp-min">${Math.round(day.temp_min)}°</span>
                </div>
                ${precipHtml}
            `;

            forecastList.appendChild(item);
        });

        weatherResult.classList.remove('hidden');
    }

    async function searchWeather() {
        const city = cityInput.value.trim();

        if (!city) {
            showError('请输入城市名称');
            return;
        }

        showLoading();

        try {
            const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
            const data = await response.json();

            if (!response.ok) {
                showError(data.error || '获取天气数据失败');
                return;
            }

            displayWeather(data);
        } catch (err) {
            showError('网络请求失败，请检查网络连接');
            console.error('Weather fetch error:', err);
        }
    }

    searchBtn.addEventListener('click', searchWeather);

    cityInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchWeather();
        }
    });

    cityInput.focus();
});
