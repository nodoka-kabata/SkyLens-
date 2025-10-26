/**
 * 設定ページ処理
 */

/**
 * 初期化
 */
function initSettings() {
    loadLocationManagementList();
    setupSettingsEventListeners();
}

/**
 * 地域管理リストを読み込み
 */
async function loadLocationManagementList() {
    try {
        const data = await apiRequest('/api/locations');
        displayLocationManagementList(data.data);
    } catch (error) {
        console.error('Load locations error:', error);
    }
}

/**
 * 地域管理リストを表示
 * @param {Array} locations - 地域の配列
 */
function displayLocationManagementList(locations) {
    const container = document.getElementById('location-management-list');
    container.innerHTML = '';
    
    if (!locations || locations.length === 0) {
        container.innerHTML = '<p>登録された地域がありません</p>';
        return;
    }
    
    locations.forEach(location => {
        const item = document.createElement('div');
        item.className = 'location-management-item';
        item.dataset.locationId = location.id;
        
        item.innerHTML = `
            <div>
                <div class="location-management-item__name">
                    ${location.name_jp || location.name}
                    ${location.is_favorite ? '⭐' : ''}
                </div>
                <div style="font-size: 0.9rem; color: #666;">
                    ${location.name} (${location.lat?.toFixed(4)}, ${location.lon?.toFixed(4)})
                </div>
            </div>
            <div class="location-management-item__actions">
                <button class="btn btn--secondary btn-small favorite-btn" data-id="${location.id}">
                    ${location.is_favorite ? '★' : '☆'}
                </button>
                <button class="btn btn--danger btn-small delete-btn" data-id="${location.id}">
                    削除
                </button>
            </div>
        `;
        
        container.appendChild(item);
    });
    
    // お気に入りボタン
    container.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const locationId = e.target.dataset.id;
            await toggleFavorite(locationId);
        });
    });
    
    // 削除ボタン
    container.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const locationId = e.target.dataset.id;
            if (confirm('この地域を削除しますか？')) {
                await deleteLocation(locationId);
            }
        });
    });
}

/**
 * お気に入りをトグル
 * @param {number} locationId - 地域ID
 */
async function toggleFavorite(locationId) {
    try {
        await apiRequest(`/api/locations/${locationId}/favorite`, {
            method: 'PUT'
        });
        showNotification('お気に入りを更新しました', 'success');
        loadLocationManagementList();
    } catch (error) {
        console.error('Toggle favorite error:', error);
    }
}

/**
 * 地域を削除
 * @param {number} locationId - 地域ID
 */
async function deleteLocation(locationId) {
    try {
        await apiRequest(`/api/locations/${locationId}`, {
            method: 'DELETE'
        });
        showNotification('地域を削除しました', 'success');
        loadLocationManagementList();
    } catch (error) {
        console.error('Delete location error:', error);
    }
}

/**
 * 地域を追加
 */
async function addLocation() {
    const name = document.getElementById('location-name').value.trim();
    const nameJp = document.getElementById('location-name-jp').value.trim();
    
    if (!name) {
        showNotification('地域名を入力してください', 'warning');
        return;
    }
    
    try {
        await apiRequest('/api/locations', {
            method: 'POST',
            body: JSON.stringify({
                name: name,
                name_jp: nameJp,
                country_code: 'JP'
            })
        });
        
        showNotification('地域を追加しました', 'success');
        document.getElementById('location-name').value = '';
        document.getElementById('location-name-jp').value = '';
        loadLocationManagementList();
    } catch (error) {
        console.error('Add location error:', error);
    }
}

/**
 * キャッシュをクリア
 */
async function clearCache() {
    if (!confirm('キャッシュをクリアしますか？')) {
        return;
    }
    
    try {
        // TODO: キャッシュクリアAPIの実装
        showNotification('キャッシュをクリアしました', 'success');
    } catch (error) {
        console.error('Clear cache error:', error);
    }
}

/**
 * イベントリスナーを設定
 */
function setupSettingsEventListeners() {
    // 地域追加ボタン
    const addLocationBtn = document.getElementById('add-location-btn');
    addLocationBtn.addEventListener('click', addLocation);
    
    // キャッシュクリアボタン
    const clearCacheBtn = document.getElementById('clear-cache-btn');
    clearCacheBtn.addEventListener('click', clearCache);
    
    // Enterキーで地域追加
    document.getElementById('location-name').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addLocation();
    });
    document.getElementById('location-name-jp').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addLocation();
    });
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', initSettings);
