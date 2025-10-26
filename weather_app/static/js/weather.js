/**
 * 天気データ処理
 */

/**
 * 天気カードを作成
 * @param {object} forecast - 天気予報データ
 * @returns {HTMLElement} 天気カード
 */
function createWeatherCard(forecast) {
    const { location, weather } = forecast;
    
    const card = document.createElement('div');
    card.className = 'weather-card';
    card.dataset.locationId = location.id;
    card.dataset.tempMax = weather.temp_max;
    card.dataset.tempMin = weather.temp_min;
    card.dataset.precipitation = weather.precipitation_probability;
    
    const precipitationClass = weather.precipitation_probability > 50 ? 'precipitation-high' : '';
    
    card.innerHTML = `
        <div class="weather-card__header">
            <div>
                <div class="weather-card__location">${location.name_jp || location.name}</div>
                <div class="weather-card__location-sub">${location.name}</div>
            </div>
            <div class="weather-card__icon">${getWeatherIcon(weather.icon_code)}</div>
        </div>
        <div class="weather-card__body">
            <div class="weather-card__description">${weather.weather_description}</div>
            <div class="weather-card__temp">
                <span class="temp-max">最高 ${formatTemperature(weather.temp_max)}</span>
                <span class="temp-min">最低 ${formatTemperature(weather.temp_min)}</span>
            </div>
            <div class="weather-card__details">
                <div class="detail-item">
                    <span>💧</span>
                    <span class="${precipitationClass}">降水: ${weather.precipitation_probability}%</span>
                </div>
                <div class="detail-item">
                    <span>💨</span>
                    <span>湿度: ${weather.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span>🌬️</span>
                    <span>風速: ${weather.wind_speed.toFixed(1)}m/s</span>
                </div>
                <div class="detail-item">
                    <span>🧭</span>
                    <span>風向: ${getWindDirection(weather.wind_deg)}</span>
                </div>
                <div class="detail-item">
                    <span>📊</span>
                    <span>気圧: ${weather.pressure}hPa</span>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * 天気カードを表示
 * @param {Array} forecasts - 天気予報データの配列
 */
function displayWeatherCards(forecasts) {
    const container = document.getElementById('weather-cards');
    container.innerHTML = '';
    
    if (!forecasts || forecasts.length === 0) {
        container.innerHTML = '<div class="loading"><p>天気データがありません</p></div>';
        return;
    }
    
    forecasts.forEach(forecast => {
        const card = createWeatherCard(forecast);
        container.appendChild(card);
    });
}

/**
 * 天気カードをソート
 * @param {string} sortBy - ソート基準
 */
function sortWeatherCards(sortBy) {
    const container = document.getElementById('weather-cards');
    const cards = Array.from(container.querySelectorAll('.weather-card'));
    
    cards.sort((a, b) => {
        switch (sortBy) {
            case 'name':
                const nameA = a.querySelector('.weather-card__location').textContent;
                const nameB = b.querySelector('.weather-card__location').textContent;
                return nameA.localeCompare(nameB, 'ja');
            
            case 'temp_max':
                return parseFloat(b.dataset.tempMax) - parseFloat(a.dataset.tempMax);
            
            case 'temp_min':
                return parseFloat(a.dataset.tempMin) - parseFloat(b.dataset.tempMin);
            
            case 'precipitation':
                return parseInt(b.dataset.precipitation) - parseInt(a.dataset.precipitation);
            
            default:
                return 0;
        }
    });
    
    container.innerHTML = '';
    cards.forEach(card => container.appendChild(card));
}

/**
 * 天気データをエクスポート
 * @param {string} format - フォーマット (csv, json)
 * @param {Array} locationIds - 地域IDの配列
 */
async function exportWeatherData(format, locationIds) {
    if (!locationIds || locationIds.length === 0) {
        showNotification('地域を選択してください', 'warning');
        return;
    }
    
    try {
        const url = `/api/weather/export?format=${format}&location_ids=${locationIds.join(',')}`;
        
        if (format === 'csv') {
            // CSVの場合はファイルダウンロード
            window.location.href = url;
            showNotification('CSVファイルをダウンロードしました', 'success');
        } else if (format === 'json') {
            // JSONの場合はデータ取得して保存
            const data = await apiRequest(url);
            const blob = new Blob([JSON.stringify(data.data.forecasts, null, 2)], {
                type: 'application/json'
            });
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `weather_forecast_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(downloadUrl);
            showNotification('JSONファイルをダウンロードしました', 'success');
        }
    } catch (error) {
        console.error('Export error:', error);
    }
}
