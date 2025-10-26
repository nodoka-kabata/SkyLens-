# GitHub Copilot 開発指示書 - お天気取得ツール

## このドキュメントについて

GitHub Copilot や各種 AI ツールが本リポジトリを効率的に開発できるよう、システム全体の設計思想・技術仕様・実装ガイドラインを統合的に記載したドキュメントです。

### 📋 利用方針
- 新機能実装時は本ガイドの技術選定・設計方針を必ず参照
- 不明点は既存コードを探索し「こういうことですか？」と確認
- 大規模変更（200行超）は事前に変更計画を提示して承認を得る
- PowerShellコマンドなどを使用する際は文字化けに気を付ける
- ファイルを破壊しないこと

### 🗣️ コミュニケーション
- **言語**: 必ず日本語で回答
- **計画提示**: 大きな変更前は「このような計画で進めます」と提案
- **確認**: 計画修正依頼があれば即座に対応・再提案

## プロジェクト概要
OpenWeatherMap APIを使用して複数地域の明日の天気予報を一覧表示するWebアプリケーション

## 技術スタック
- **バックエンド**: Python 3.8+ / Flask 2.3+
- **フロントエンド**: HTML5, CSS3 (Grid/Flexbox), Vanilla JavaScript (ES6+)
- **データベース**: SQLite 3
- **外部API**: OpenWeatherMap API v2.5
- **主要ライブラリ**: SQLAlchemy, Requests, APScheduler, Cryptography

## コーディング規約

### Python コード規約
```python
# PEP 8 準拠、型ヒント必須
from typing import List, Dict, Optional
from datetime import datetime

def get_weather_forecast(location_id: int, date: datetime) -> Optional[Dict]:
    """
    指定された地域の天気予報を取得
    
    Args:
        location_id: 地域ID
        date: 予報日時
        
    Returns:
        天気予報データの辞書、エラー時はNone
        
    Raises:
        ValueError: 無効な地域IDの場合
    """
    pass

# クラス名: PascalCase
class WeatherService:
    pass

# 関数名・変数名: snake_case
def fetch_api_data():
    user_name = "test"
    
# 定数: UPPER_SNAKE_CASE
API_BASE_URL = "https://api.openweathermap.org/data/2.5"
MAX_LOCATIONS = 10
```

### JavaScript コード規約
```javascript
// ES6+ モダンシンタックス使用、関数型プログラミング推奨
// 変数: const優先、必要に応じてlet、var禁止
const API_ENDPOINT = '/api/weather/forecast';

// 関数: camelCase
async function fetchWeatherData(locationIds) {
    try {
        const response = await fetch(`${API_ENDPOINT}?ids=${locationIds.join(',')}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('天気データの取得に失敗:', error);
        return null;
    }
}

// アロー関数の活用
const formatTemperature = (temp) => `${temp.toFixed(1)}°C`;

// 分割代入の活用
const { temp_max, temp_min, humidity } = weatherData;
```

### CSS コード規約
```css
/* BEM命名規則を推奨 */
.weather-card { }
.weather-card__header { }
.weather-card__body { }
.weather-card--featured { }

/* CSS変数の活用 */
:root {
    --primary-color: #2196F3;
    --spacing-unit: 8px;
}

/* モバイルファースト、レスポンシブ */
.container {
    width: 100%;
}

@media (min-width: 768px) {
    .container {
        max-width: 720px;
    }
}
```

## ディレクトリ構造とファイル配置
```
weather_app/
├── app.py                    # Flaskアプリケーションエントリーポイント
├── config.py                 # 設定管理（環境変数読み込み）
├── requirements.txt          # pip依存関係
├── models/
│   ├── __init__.py
│   ├── weather.py           # WeatherForecast モデル
│   └── location.py          # Location モデル
├── views/
│   ├── __init__.py
│   ├── main.py              # メインページルート
│   └── api.py               # RESTful APIエンドポイント
├── services/
│   ├── __init__.py
│   ├── weather_service.py   # OpenWeatherMap API連携
│   └── data_service.py      # DB操作ロジック
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js          # 初期化・イベント設定
│   │   ├── weather.js       # 天気データ処理
│   │   └── utils.js         # ユーティリティ関数
│   └── images/
│       └── weather-icons/
├── templates/
│   ├── base.html            # 共通レイアウト
│   ├── index.html           # メインページ
│   └── settings.html        # 設定ページ
└── tests/
    └── test_*.py            # pytestテストファイル
```

## API設計仕様

### OpenWeatherMap API呼び出し
```python
# エンドポイント
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# リクエストパラメータ
params = {
    'q': 'Tokyo,JP',           # 都市名,国コード
    'appid': API_KEY,          # APIキー
    'units': 'metric',         # 温度単位（metric=摂氏）
    'lang': 'ja',              # 言語（日本語）
    'cnt': 8                   # データポイント数（8=24時間分）
}

# レスポンス構造
{
    "list": [
        {
            "dt": 1698566400,
            "main": {
                "temp": 20.5,
                "temp_min": 18.2,
                "temp_max": 22.3,
                "humidity": 65,
                "pressure": 1013
            },
            "weather": [
                {
                    "main": "Clear",
                    "description": "晴天",
                    "icon": "01d"
                }
            ],
            "wind": {
                "speed": 3.5,
                "deg": 180
            },
            "pop": 0.1  # 降水確率
        }
    ]
}
```

### 内部REST API仕様
```
GET /api/weather/forecast?location_ids=1,2,3&date=2025-10-20
Response: 200 OK
{
    "status": "success",
    "data": {
        "forecasts": [...]
    }
}

POST /api/weather/refresh
Request Body: {"location_ids": [1, 2, 3]}
Response: 200 OK

GET /api/weather/export?format=csv&location_ids=1,2,3
Response: 200 OK (file download)

GET /api/locations
POST /api/locations {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503}
PUT /api/locations/1/favorite {"is_favorite": true}
DELETE /api/locations/1
```

## データベーススキーマ

### SQLAlchemy モデル定義例
```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    name_jp = Column(String(100))
    lat = Column(Float)
    lon = Column(Float)
    country_code = Column(String(2))
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class WeatherForecast(Base):
    __tablename__ = 'weather_forecasts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    forecast_date = Column(DateTime, nullable=False)
    weather_main = Column(String(50))
    weather_description = Column(String(100))
    temp_max = Column(Float)
    temp_min = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    precipitation_probability = Column(Integer)
    icon_code = Column(String(10))
    fetched_at = Column(DateTime, default=datetime.utcnow)
```

## エラーハンドリングパターン

### バックエンド（Python）
```python
# カスタム例外クラス
class WeatherAPIError(Exception):
    """天気APIエラー"""
    pass

class DatabaseError(Exception):
    """データベースエラー"""
    pass

# エラーハンドリング例
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'error_code': 'NOT_FOUND',
        'message': 'リソースが見つかりません'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Internal Server Error: {error}')
    return jsonify({
        'status': 'error',
        'error_code': 'INTERNAL_ERROR',
        'message': 'サーバーエラーが発生しました'
    }), 500

# サービス層でのエラーハンドリング
def fetch_weather_from_api(location: str) -> dict:
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise WeatherAPIError("APIタイムアウト")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise WeatherAPIError("APIキーが無効です")
        elif e.response.status_code == 429:
            raise WeatherAPIError("API制限に達しました")
        else:
            raise WeatherAPIError(f"APIエラー: {e}")
    except Exception as e:
        app.logger.error(f"予期しないエラー: {e}")
        raise
```

### フロントエンド（JavaScript）
```javascript
// グローバルエラーハンドラー
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showNotification('エラーが発生しました', 'error');
});

// API呼び出しエラーハンドリング
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

// ユーザー通知関数
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 5000);
}
```

## セキュリティ要件

### APIキー管理
```python
# 環境変数から読み込み
import os
from cryptography.fernet import Fernet

# .envファイル使用（本番環境では環境変数）
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# APIキー暗号化保存
def encrypt_api_key(api_key: str) -> str:
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(api_key.encode()).decode()

# .gitignoreに必ず追加
"""
.env
config.json
*.db
__pycache__/
*.pyc
"""
```

### CSRF/XSS対策
```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

# テンプレートでのエスケープ（Jinja2自動）
# {{ user_input }}  # 自動エスケープ
# {{ user_input | safe }}  # エスケープ無効化（使用注意）
```

## パフォーマンス最適化

### データベースクエリ最適化
```python
# インデックス定義
class WeatherForecast(Base):
    __table_args__ = (
        Index('idx_location_date', 'location_id', 'forecast_date'),
    )

# N+1問題回避（eager loading）
from sqlalchemy.orm import joinedload

locations = db.session.query(Location).options(
    joinedload(Location.weather_forecasts)
).all()

# バッチ挿入
db.session.bulk_insert_mappings(WeatherForecast, forecast_data_list)
db.session.commit()
```

### フロントエンド最適化
```javascript
// デバウンス処理
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// 検索入力にデバウンス適用
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', debounce((e) => {
    searchLocations(e.target.value);
}, 300));

// 画像遅延読み込み
document.querySelectorAll('img[data-src]').forEach(img => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });
    observer.observe(img);
});
```

## テストパターン

### pytest例
```python
import pytest
from app import create_app, db
from models.location import Location

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_locations(client):
    response = client.get('/api/locations')
    assert response.status_code == 200
    assert 'data' in response.json

def test_add_location(client):
    data = {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503}
    response = client.post('/api/locations', json=data)
    assert response.status_code == 201
```

## 開発ワークフロー

1. **機能実装前**: 該当する設計書（basic_design.md）を確認
2. **コード作成**: 本指示書の規約に従う
3. **ユニットテスト**: 関数・クラス単位でテスト作成
4. **コミット**: 明確なコミットメッセージ（日本語可）
5. **動作確認**: ブラウザでの実際の動作確認

## コミットメッセージ規約
```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント変更
style: コードスタイル修正（機能変更なし）
refactor: リファクタリング
test: テスト追加・修正
chore: ビルドプロセス・補助ツール変更

例:
feat: 地域選択機能を追加
fix: APIタイムアウト時のエラーハンドリングを修正
docs: README.mdにセットアップ手順を追加
```

## よく使う日本の主要都市座標
```python
PRESET_LOCATIONS = [
    {'name': 'Tokyo', 'name_jp': '東京', 'lat': 35.6762, 'lon': 139.6503},
    {'name': 'Osaka', 'name_jp': '大阪', 'lat': 34.6937, 'lon': 135.5023},
    {'name': 'Nagoya', 'name_jp': '名古屋', 'lat': 35.1815, 'lon': 136.9066},
    {'name': 'Sapporo', 'name_jp': '札幌', 'lat': 43.0642, 'lon': 141.3469},
    {'name': 'Fukuoka', 'name_jp': '福岡', 'lat': 33.5904, 'lon': 130.4017},
    {'name': 'Sendai', 'name_jp': '仙台', 'lat': 38.2682, 'lon': 140.8694},
    {'name': 'Hiroshima', 'name_jp': '広島', 'lat': 34.3853, 'lon': 132.4553},
    {'name': 'Kyoto', 'name_jp': '京都', 'lat': 35.0116, 'lon': 135.7681},
]
```

## 重要な注意事項

⚠️ **必ず守ること**:
1. APIキーは環境変数で管理、ハードコード禁止
2. SQLインジェクション対策（SQLAlchemy ORM使用）
3. 全ての外部入力をバリデーション
4. エラー時は必ずログ出力
5. 機密情報をコミットしない（.gitignore確認）

✅ **推奨事項**:
1. 関数は単一責任の原則に従う
2. マジックナンバーは定数化
3. コメントは「なぜ」を書く（「何を」はコードで表現）
4. 複雑なロジックは関数に分割
5. 定期的にリファクタリング

---

**作成日**: 2025年10月27日  
**更新日**: 2025年10月27日  
**バージョン**: 1.0