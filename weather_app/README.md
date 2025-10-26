# お天気取得ツール

OpenWeatherMap APIを使用して複数地域の明日の天気予報を一覧表示するWebアプリケーション

## 🌟 主な機能

- 📍 複数地域（最大10箇所）の天気予報を同時に表示
- 🌤️ 明日の天気情報（天気、最高/最低気温、降水確率、湿度、風速など）
- 🗾 日本の主要都市8箇所がプリセット登録済み
- ⭐ お気に入り地域の管理
- 📊 地域名・気温・降水確率でのソート機能
- 📥 CSV/JSON形式でのデータエクスポート
- 📱 レスポンシブデザイン対応

## 🚀 セットアップ

### 必要な環境

- Python 3.8以上
- pip

### インストール手順

1. **リポジトリのクローン**

```bash
cd weather_app
```

2. **仮想環境の作成（推奨）**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **依存ライブラリのインストール**

```powershell
pip install -r requirements.txt
```

4. **環境変数の設定**

`.env.example`を`.env`にコピーして、APIキーを設定します：

```powershell
Copy-Item .env.example .env
```

`.env`ファイルを編集：

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### OpenWeatherMap APIキーの取得

1. [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) でアカウントを作成
2. [APIキー管理ページ](https://home.openweathermap.org/api_keys) でAPIキーを取得
3. `.env`ファイルに設定

## 🎮 使い方

### サーバーの起動

```powershell
python app.py
```

ブラウザで http://localhost:5000 にアクセス

### 基本的な使い方

1. **地域選択**
   - プリセット地域から選択（複数選択可、最大10地域）
   - 選択した地域は青色でハイライト表示

2. **天気データの取得**
   - 「🔄 天気を更新」ボタンをクリック
   - APIから最新の天気データを取得して表示

3. **データのエクスポート**
   - 「📥 CSV出力」: CSV形式でダウンロード
   - 「📥 JSON出力」: JSON形式でダウンロード

4. **ソート**
   - ドロップダウンから並び替え基準を選択
   - 地域名順・最高気温順・最低気温順・降水確率順

### 設定ページ

http://localhost:5000/settings にアクセス

- **地域管理**: 新しい地域の追加・削除
- **お気に入り**: 地域をお気に入り登録
- **データ管理**: キャッシュのクリア

## 📁 プロジェクト構造

```
weather_app/
├── app.py                    # メインアプリケーション
├── config.py                 # 設定管理
├── requirements.txt          # 依存ライブラリ
├── .env                      # 環境変数（要作成）
├── models/                   # データモデル
│   ├── __init__.py
│   ├── location.py          # 地域モデル
│   └── weather.py           # 天気予報モデル
├── views/                    # ビューコントローラー
│   ├── __init__.py
│   ├── main.py              # メインページ
│   └── api.py               # APIエンドポイント
├── services/                 # ビジネスロジック
│   ├── __init__.py
│   ├── weather_service.py   # 天気API連携
│   └── data_service.py      # データ管理
├── static/                   # 静的ファイル
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── weather.js
│       ├── settings.js
│       └── utils.js
├── templates/                # HTMLテンプレート
│   ├── base.html
│   ├── index.html
│   └── settings.html
└── data/                     # データベース（自動作成）
    └── weather.db
```

## 🛠️ 技術スタック

- **バックエンド**: Flask 3.0
- **データベース**: SQLite3 + SQLAlchemy
- **フロントエンド**: HTML5, CSS3, Vanilla JavaScript
- **API**: OpenWeatherMap API v2.5

## 📡 APIエンドポイント

### 地域管理

- `GET /api/locations` - 全地域取得
- `POST /api/locations` - 地域追加
- `DELETE /api/locations/<id>` - 地域削除
- `PUT /api/locations/<id>/favorite` - お気に入りトグル

### 天気予報

- `GET /api/weather/forecast` - 天気予報取得
- `POST /api/weather/refresh` - 天気データ更新
- `GET /api/weather/export` - データエクスポート

## 🎨 プリセット地域

- 東京 (Tokyo)
- 大阪 (Osaka)
- 名古屋 (Nagoya)
- 札幌 (Sapporo)
- 福岡 (Fukuoka)
- 仙台 (Sendai)
- 広島 (Hiroshima)
- 京都 (Kyoto)

## 🐛 トラブルシューティング

### APIキーエラー

```
APIキーが無効です
```

→ `.env`ファイルのAPIキーを確認してください

### 地域が見つからない

```
地域が見つかりません: CityName
```

→ 英語の地域名で正確に入力してください

### API制限エラー

```
API制限に達しました
```

→ 無料プランは1日1000回まで。時間をおいて再試行してください

## 📝 開発情報

### コミットメッセージ規約

本プロジェクトは Conventional Commits に準拠します。

- 形式: `<type>(<scope>)<!>: <subject>`
- 主な type: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- 例: `feat(services): 明日の最高/最低の計算をtemp_max/minから集計`
- 詳細は `.github/COMMIT_CONVENTION.md` を参照

任意でテンプレートを使う場合は、ルートの `.gitmessage` を設定してください（1回のみ）。

```powershell
git config commit.template .gitmessage
```

### コーディング規約

- Python: PEP 8準拠
- JavaScript: ES6+、const優先
- CSS: BEM命名規則

詳細は `.github/copilot-instructions.md` を参照

### テスト実行

```powershell
pytest tests/
```

## 📄 ライセンス

MIT License

## 👤 作成者

AI Assistant

## 🙏 謝辞

- [OpenWeatherMap](https://openweathermap.org/) - 天気データAPI提供
- [Flask](https://flask.palletsprojects.com/) - Webフレームワーク

---

**更新日**: 2025年10月27日  
**バージョン**: 1.0.0
