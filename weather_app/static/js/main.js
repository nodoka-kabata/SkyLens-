/**
 * メイン処理
 */

let selectedLocationIds = [];
let allLocations = [];
let searchDebounceTimer = null;

/**
 * 初期化
 */
async function init() {
    try {
        // 地域リストを取得
        await loadLocations();
        
        // イベントリスナー設定
        setupEventListeners();
        
        showNotification('アプリケーションを起動しました', 'success');
    } catch (error) {
        console.error('Initialization error:', error);
        showNotification('初期化に失敗しました', 'error');
    }
}

/**
 * 地域リストを読み込み
 */
async function loadLocations() {
    try {
        const data = await apiRequest('/api/locations');
        allLocations = data.data;
        displayLocationList(allLocations);
    } catch (error) {
        console.error('Load locations error:', error);
    }
}

/**
 * 地域リストを表示
 * @param {Array} locations - 地域の配列
 */
function displayLocationList(locations) {
    const container = document.getElementById('location-list');
    container.innerHTML = '';
    
    locations.forEach(location => {
        const item = document.createElement('div');
        item.className = 'location-item';
        item.dataset.locationId = location.id;
        
        item.innerHTML = `
            <div class="location-item__name">${location.name}</div>
            <div class="location-item__name-jp">${location.name_jp || ''}</div>
        `;
        
        item.addEventListener('click', () => toggleLocationSelection(location.id, item));
        
        container.appendChild(item);
    });
}

/**
 * 地域選択をトグル
 * @param {number} locationId - 地域ID
 * @param {HTMLElement} element - 要素
 */
function toggleLocationSelection(locationId, element) {
    const index = selectedLocationIds.indexOf(locationId);
    
    if (index > -1) {
        // 選択解除
        selectedLocationIds.splice(index, 1);
        element.classList.remove('selected');
    } else {
        // 選択
        if (selectedLocationIds.length >= 10) {
            showNotification('最大10地域まで選択できます', 'warning');
            return;
        }
        selectedLocationIds.push(locationId);
        element.classList.add('selected');
    }
}

/**
 * 天気データを更新
 */
async function refreshWeatherData() {
    if (selectedLocationIds.length === 0) {
        showNotification('地域を選択してください', 'warning');
        return;
    }
    
    try {
        const refreshBtn = document.getElementById('refresh-btn');
        refreshBtn.disabled = true;
        refreshBtn.textContent = '⏳ 更新中...';
        
        // 天気データを取得
        const data = await apiRequest('/api/weather/refresh', {
            method: 'POST',
            body: JSON.stringify({ location_ids: selectedLocationIds })
        });
        
        if (data.status === 'success' && data.data.forecasts.length > 0) {
            displayWeatherCards(data.data.forecasts);
            showNotification(data.message || '天気データを更新しました', 'success');
            
            if (data.errors && data.errors.length > 0) {
                data.errors.forEach(error => {
                    showNotification(error, 'warning');
                });
            }
        } else {
            showNotification('天気データの取得に失敗しました', 'error');
        }
    } catch (error) {
        console.error('Refresh error:', error);
    } finally {
        const refreshBtn = document.getElementById('refresh-btn');
        refreshBtn.disabled = false;
        refreshBtn.textContent = '🔄 天気を更新';
    }
}

/**
 * イベントリスナーを設定
 */
/**
 * 地域を検索（入力中にリアルタイム検索）
 */
async function searchLocations(query = null) {
    const searchInput = document.getElementById('location-search-input');
    const searchQuery = query || searchInput.value.trim();
    const resultsContainer = document.getElementById('search-results');
    
    // 空の場合は結果をクリア
    if (!searchQuery) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    // 最低2文字から検索
    if (searchQuery.length < 2) {
        resultsContainer.innerHTML = '<div class="search-results-empty">2文字以上入力してください</div>';
        return;
    }
    
    try {
        const data = await apiRequest(`/api/locations/search?q=${encodeURIComponent(searchQuery)}&limit=5`);
        displaySearchResults(data.data);
        
        if (data.data.length === 0) {
            resultsContainer.innerHTML = '<div class="search-results-empty">該当する地域が見つかりませんでした</div>';
        }
    } catch (error) {
        console.error('Search error:', error);
        resultsContainer.innerHTML = '<div class="search-results-empty">検索中にエラーが発生しました</div>';
    }
}

/**
 * デバウンス付き検索（入力が止まってから実行）
 */
function debouncedSearch() {
    // 既存のタイマーをクリア
    if (searchDebounceTimer) {
        clearTimeout(searchDebounceTimer);
    }
    
    // 300ms後に検索実行
    searchDebounceTimer = setTimeout(() => {
        searchLocations();
    }, 300);
}

/**
 * 検索結果を表示
 * @param {Array} results - 検索結果の配列
 */
function displaySearchResults(results) {
    const container = document.getElementById('search-results');
    container.innerHTML = '';
    
    if (!results || results.length === 0) {
        container.innerHTML = '<div class="search-results-empty">検索結果がありません</div>';
        return;
    }
    
    results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        
        // 日本語名を取得
        const localName = result.local_names?.ja || result.local_names?.en || result.name;
        
        // 地域情報を表示
        const locationInfo = [];
        if (result.state) locationInfo.push(`${result.state}`);
        if (result.country) locationInfo.push(`${result.country}`);
        locationInfo.push(`${result.lat.toFixed(4)}, ${result.lon.toFixed(4)}`);
        
        item.innerHTML = `
            <div class="search-result-item__name">${result.name} ${localName !== result.name ? `(${localName})` : ''}</div>
            <div class="search-result-item__details">
                ${locationInfo.map(info => `<span>${info}</span>`).join('')}
            </div>
        `;
        
        // クリックで地域を追加
        item.addEventListener('click', () => addLocationFromSearch(result));
        
        container.appendChild(item);
    });
}

/**
 * 検索結果から地域を追加
 * @param {Object} location - 地域情報
 */
async function addLocationFromSearch(location) {
    try {
        // 既に存在するか確認
        const existing = allLocations.find(loc => 
            loc.name === location.name && 
            Math.abs(loc.lat - location.lat) < 0.01 && 
            Math.abs(loc.lon - location.lon) < 0.01
        );
        
        if (existing) {
            showNotification(`${location.name}は既に登録されています`, 'info');
            return;
        }
        
        // 地域を追加
        const localName = location.local_names?.ja || location.local_names?.en || '';
        const data = await apiRequest('/api/locations', {
            method: 'POST',
            body: JSON.stringify({
                name: location.name,
                name_jp: localName,
                lat: location.lat,
                lon: location.lon,
                country_code: location.country
            })
        });
        
        showNotification(`${location.name}を追加しました`, 'success');
        
        // 地域リストを再読み込み
        await loadLocations();
        
        // 検索結果をクリア
        document.getElementById('search-results').innerHTML = '';
        document.getElementById('location-search-input').value = '';
        
    } catch (error) {
        console.error('Add location error:', error);
    }
}

/**
 * イベントリスナーを設定
 */
function setupEventListeners() {
    // 地域検索入力（リアルタイム検索）
    const searchInput = document.getElementById('location-search-input');
    searchInput.addEventListener('input', debouncedSearch);
    
    // 地域検索ボタン
    const searchBtn = document.getElementById('search-btn');
    searchBtn.addEventListener('click', () => searchLocations());
    
    // Enterキーで検索
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            // デバウンスタイマーをクリアして即座に検索
            if (searchDebounceTimer) {
                clearTimeout(searchDebounceTimer);
            }
            searchLocations();
        }
    });
    
    // 天気更新ボタン
    const refreshBtn = document.getElementById('refresh-btn');
    refreshBtn.addEventListener('click', refreshWeatherData);
    
    // CSVエクスポートボタン
    const exportCsvBtn = document.getElementById('export-csv-btn');
    exportCsvBtn.addEventListener('click', () => {
        exportWeatherData('csv', selectedLocationIds);
    });
    
    // JSONエクスポートボタン
    const exportJsonBtn = document.getElementById('export-json-btn');
    exportJsonBtn.addEventListener('click', () => {
        exportWeatherData('json', selectedLocationIds);
    });
    
    // ソート選択
    const sortSelect = document.getElementById('sort-select');
    sortSelect.addEventListener('change', (e) => {
        sortWeatherCards(e.target.value);
    });
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', init);
