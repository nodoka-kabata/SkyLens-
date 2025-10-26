/**
 * ユーティリティ関数
 */

/**
 * 通知を表示
 * @param {string} message - メッセージ
 * @param {string} type - タイプ (success, error, warning, info)
 */
function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    // 5秒後に自動削除
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * API呼び出し
 * @param {string} url - URL
 * @param {object} options - オプション
 * @returns {Promise} レスポンス
 */
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error(`API Error [${url}]:`, error);
        showNotification(error.message, 'error');
        throw error;
    }
}

/**
 * 天気アイコンの取得
 * @param {string} iconCode - アイコンコード
 * @returns {string} アイコンの絵文字
 */
function getWeatherIcon(iconCode) {
    const iconMap = {
        '01d': '☀️', '01n': '🌙',
        '02d': '⛅', '02n': '☁️',
        '03d': '☁️', '03n': '☁️',
        '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️',
        '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️',
        '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
    };
    return iconMap[iconCode] || '🌤️';
}

/**
 * 温度のフォーマット
 * @param {number} temp - 温度
 * @returns {string} フォーマットされた温度
 */
function formatTemperature(temp) {
    return `${temp.toFixed(1)}°C`;
}

/**
 * 風向の変換
 * @param {number} deg - 角度
 * @returns {string} 風向
 */
function getWindDirection(deg) {
    const directions = ['北', '北東', '東', '南東', '南', '南西', '西', '北西'];
    const index = Math.round(deg / 45) % 8;
    return directions[index];
}

/**
 * デバウンス処理
 * @param {Function} func - 関数
 * @param {number} wait - 待機時間（ミリ秒）
 * @returns {Function} デバウンスされた関数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// CSSアニメーション追加
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
