# 環境構築手順

## ✅ 完了した作業

### 1. 仮想環境の作成 ✓
```powershell
python -m venv venv
```

### 2. 仮想環境の有効化 ✓
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. 依存ライブラリのインストール ✓
以下のパッケージをインストールしました：
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- requests==2.31.0
- python-dotenv==1.0.0
- APScheduler==3.10.4
- cryptography==41.0.7

### 4. 環境変数ファイルの作成 ✓
- `.env`ファイルを作成
- Flask用のシークレットキーを自動生成して設定

## 🔑 次のステップ: OpenWeatherMap APIキーの設定

### APIキーの取得方法

1. **OpenWeatherMapにアカウント登録**
   - https://home.openweathermap.org/users/sign_up にアクセス
   - メールアドレスとパスワードでアカウント作成

2. **APIキーの取得**
   - ログイン後、https://home.openweathermap.org/api_keys にアクセス
   - デフォルトのAPIキーが表示されます
   - または「Generate」ボタンで新しいキーを生成

3. **APIキーを`.env`ファイルに設定**

`.env`ファイルを開いて、以下の行を編集してください：

```env
OPENWEATHER_API_KEY=your_api_key_here
```

↓

```env
OPENWEATHER_API_KEY=取得したAPIキーをここに貼り付け
```

## 🚀 アプリケーションの起動

APIキーを設定したら、以下のコマンドで起動できます：

```powershell
python app.py
```

ブラウザで http://localhost:5000 にアクセスしてください！

## 📝 確認事項

- ✅ Python 3.10.11 使用中
- ✅ 仮想環境: `d:\CAIND\お天気取得ツール\.venv`
- ✅ 依存ライブラリ: インストール済み
- ✅ `.env`ファイル: 作成済み
- ⚠️ **OpenWeatherMap APIキー: 要設定**

## ⚡ クイックスタート

```powershell
# APIキーを設定してから実行
python app.py
```

---
**環境構築日**: 2025年10月27日
