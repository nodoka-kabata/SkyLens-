# お天気取得ツール 基本設計書（Webアプリケーション版）

## 1. システム概要

### 1.1 システム構成
- **アーキテクチャ**: MVC（Model-View-Controller）パターン
- **フロントエンド**: HTML5 + CSS3 + JavaScript（ES6+）
- **バックエンド**: Python Flask
- **データベース**: SQLite
- **外部API**: OpenWeatherMap API

### 1.2 システム構成図
```
[ブラウザ] <-- HTTP --> [Flask Webサーバー] <-- API --> [OpenWeatherMap]
                              |
                         [SQLiteDB]
                              |
                         [ローカルファイル]
```

## 2. アーキテクチャ設計

### 2.1 ディレクトリ構成
```
weather_app/
├── app.py                    # メインアプリケーション
├── config.py                 # 設定ファイル
├── requirements.txt          # 依存ライブラリ
├── models/
│   ├── __init__.py
│   ├── weather.py           # 天気データモデル
│   └── location.py          # 地域データモデル
├── views/
│   ├── __init__.py
│   ├── main.py              # メインビュー
│   └── api.py               # APIエンドポイント
├── services/
│   ├── __init__.py
│   ├── weather_service.py   # 天気データ取得サービス
│   └── data_service.py      # データ管理サービス
├── static/
│   ├── css/
│   │   ├── style.css        # メインスタイル
│   │   └── responsive.css   # レスポンシブ対応
│   ├── js/
│   │   ├── main.js          # メイン処理
│   │   ├── weather.js       # 天気データ処理
│   │   └── utils.js         # ユーティリティ
│   └── images/
│       └── weather-icons/   # 天気アイコン
├── templates/
│   ├── base.html           # ベーステンプレート
│   ├── index.html          # メインページ
│   ├── settings.html       # 設定ページ
│   └── history.html        # 履歴ページ
├── data/
│   ├── weather.db          # SQLiteデータベース
│   └── config.json         # 設定ファイル
└── tests/
    ├── test_weather_service.py
    ├── test_data_service.py
    └── test_views.py
```

### 2.2 技術スタック

#### 2.2.1 バックエンド
- **Flask**: Webフレームワーク
- **SQLAlchemy**: ORM
- **Requests**: HTTP通信
- **APScheduler**: スケジューラー
- **Cryptography**: 暗号化

#### 2.2.2 フロントエンド
- **HTML5**: マークアップ
- **CSS3**: スタイリング（Grid/Flexbox使用）
- **JavaScript**: 動的処理
- **Chart.js**: グラフ表示（オプション）
- **Bootstrap**: UIフレームワーク（オプション）

## 3. データベース設計

### 3.1 テーブル構成

#### 3.1.1 locations テーブル
```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    name_jp VARCHAR(100),
    lat DECIMAL(10,8),
    lon DECIMAL(11,8),
    country_code VARCHAR(2),
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.2 weather_forecasts テーブル
```sql
CREATE TABLE weather_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    forecast_date DATE,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    temp_max DECIMAL(5,2),
    temp_min DECIMAL(5,2),
    humidity INTEGER,
    pressure INTEGER,
    wind_speed DECIMAL(5,2),
    wind_deg INTEGER,
    precipitation_probability INTEGER,
    icon_code VARCHAR(10),
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);
```

#### 3.1.3 user_settings テーブル
```sql
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(50) UNIQUE,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.4 search_history テーブル
```sql
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_ids TEXT,  -- JSON形式で複数のlocation_idを格納
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. API設計

### 4.1 RESTful API エンドポイント

#### 4.1.1 天気予報関連API
```
GET /api/weather/forecast
- パラメータ: location_ids (カンマ区切り), date (YYYY-MM-DD)
- レスポンス: 指定地域の天気予報データ

POST /api/weather/refresh
- パラメータ: location_ids (カンマ区切り)
- レスポンス: 最新の天気予報データ取得結果

GET /api/weather/export
- パラメータ: format (csv|json), location_ids, date
- レスポンス: ファイルダウンロード
```

#### 4.1.2 地域管理API
```
GET /api/locations
- レスポンス: 利用可能な地域一覧

POST /api/locations
- パラメータ: name, lat, lon
- レスポンス: 地域追加結果

PUT /api/locations/{id}/favorite
- レスポンス: お気に入り設定結果

DELETE /api/locations/{id}
- レスポンス: 地域削除結果
```

#### 4.1.3 設定管理API
```
GET /api/settings
- レスポンス: 現在の設定値

PUT /api/settings
- パラメータ: settings (JSON)
- レスポンス: 設定更新結果
```

### 4.2 レスポンス形式

#### 4.2.1 成功レスポンス
```json
{
    "status": "success",
    "data": {
        "forecasts": [
            {
                "location": {
                    "id": 1,
                    "name": "Tokyo",
                    "name_jp": "東京"
                },
                "weather": {
                    "date": "2025-10-20",
                    "main": "Clear",
                    "description": "晴天",
                    "temp_max": 25.5,
                    "temp_min": 18.2,
                    "humidity": 60,
                    "precipitation_probability": 10,
                    "wind_speed": 3.2,
                    "icon": "01d"
                }
            }
        ]
    },
    "message": "天気予報を正常に取得しました"
}
```

#### 4.2.2 エラーレスポンス
```json
{
    "status": "error",
    "error_code": "API_LIMIT_EXCEEDED",
    "message": "APIの利用制限に達しました",
    "details": {
        "retry_after": 3600
    }
}
```

## 5. 画面設計

### 5.1 画面構成

#### 5.1.1 メイン画面 (index.html)
- **ヘッダー**: アプリタイトル、設定ボタン、更新ボタン
- **地域選択エリア**: 
  - プリセット地域ボタン
  - 地域検索入力フィールド
  - 選択済み地域リスト
- **天気予報表示エリア**:
  - 地域別天気情報カード
  - ソート・フィルター機能
- **フッター**: エクスポートボタン、履歴ボタン

#### 5.1.2 設定画面 (settings.html)
- **API設定**: APIキー入力・保存
- **表示設定**: 単位選択、言語選択
- **更新設定**: 自動更新間隔設定
- **データ管理**: キャッシュクリア、履歴削除

#### 5.1.3 履歴画面 (history.html)
- **検索履歴**: 過去の検索パターン表示
- **お気に入り地域**: よく使用する地域管理

### 5.2 UI/UXデザイン指針

#### 5.2.1 デザインコンセプト
- **シンプル**: 直感的で分かりやすいインターフェース
- **レスポンシブ**: デスクトップ・タブレット・スマートフォン対応
- **アクセシブル**: 色覚特性やスクリーンリーダー対応

#### 5.2.2 カラーパレット
```css
:root {
    --primary-color: #2196F3;     /* メインブルー */
    --secondary-color: #FFC107;   /* アクセントイエロー */
    --success-color: #4CAF50;     /* 成功グリーン */
    --warning-color: #FF9800;     /* 警告オレンジ */
    --error-color: #F44336;       /* エラーレッド */
    --background-color: #F5F5F5;  /* 背景グレー */
    --text-color: #333333;        /* テキストダーク */
    --card-background: #FFFFFF;   /* カード背景ホワイト */
}
```

## 6. システム処理フロー

### 6.1 天気予報取得フロー
```
1. ユーザーが地域を選択
2. フロントエンドがAJAXでAPIリクエスト
3. バックエンドがOpenWeatherMap APIを呼び出し
4. データをデータベースに保存
5. 整形したデータをJSONで返却
6. フロントエンドが画面を更新
```

### 6.2 データ更新フロー
```
1. APSchedulerが定期実行トリガー
2. お気に入り地域の天気データを自動取得
3. 古いデータを削除（7日以上前）
4. WebSocketで接続中クライアントに通知（オプション）
```

## 7. セキュリティ設計

### 7.1 セキュリティ対策

#### 7.1.1 データ保護
- **APIキー暗号化**: Fernet暗号化でAPIキーを保存
- **CSRF対策**: Flask-WTFでCSRFトークン使用
- **XSS対策**: テンプレートエンジンでエスケープ処理

#### 7.1.2 通信セキュリティ
- **HTTPS**: 本番環境ではHTTPS必須
- **API制限**: レート制限機能実装
- **入力検証**: 全ての入力データの検証

### 7.2 エラーハンドリング
```python
# エラーハンドリングの例
try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    return {"error": "API_TIMEOUT", "message": "APIのタイムアウトが発生しました"}
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        return {"error": "INVALID_API_KEY", "message": "APIキーが無効です"}
    elif e.response.status_code == 429:
        return {"error": "RATE_LIMIT", "message": "API制限に達しました"}
```

## 8. パフォーマンス設計

### 8.1 最適化戦略

#### 8.1.1 データベース最適化
- インデックス設定（location_id, forecast_date）
- 古いデータの自動削除
- クエリ最適化

#### 8.1.2 API最適化
- リクエストの並列処理
- キャッシュ機能（Redis使用を検討）
- 差分更新

#### 8.1.3 フロントエンド最適化
- 画像最適化（WebP形式使用）
- CSS/JSファイルの圧縮
- 遅延読み込み（Lazy Loading）

## 9. テスト設計

### 9.1 テスト戦略

#### 9.1.1 ユニットテスト
- モデルクラスのテスト
- サービスクラスのテスト
- ユーティリティ関数のテスト

#### 9.1.2 統合テスト
- API エンドポイントのテスト
- データベース操作のテスト
- 外部API連携のテスト

#### 9.1.3 E2Eテスト
- ブラウザ自動化テスト（Seleniumを検討）
- ユーザーシナリオテスト

## 10. デプロイメント設計

### 10.1 開発環境
- **ローカル開発**: Flask開発サーバー
- **データベース**: SQLite

### 10.2 本番環境
- **Webサーバー**: Gunicorn + Nginx
- **データベース**: SQLite または PostgreSQL
- **プロセス管理**: systemd
- **ログ管理**: Python logging + logrotate

### 10.3 デプロイメントスクリプト
```bash
#!/bin/bash
# deploy.sh
git pull origin main
pip install -r requirements.txt
python -m flask db upgrade
sudo systemctl restart weather-app
sudo systemctl reload nginx
```

## 11. 監視・運用設計

### 11.1 ログ設計
```python
import logging

# ログ設定例
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/weather_app.log'),
        logging.StreamHandler()
    ]
)
```

### 11.2 監視項目
- APIレスポンス時間
- エラー発生率
- データベース接続状態
- ディスク使用量

---

**作成日**: 2025年10月19日  
**バージョン**: 1.0  
**作成者**: AI Assistant