"""
お天気取得ツール - Flaskアプリケーション
"""
from flask import Flask
from models import db
from views.main import main_bp
from views.api import api_bp
from config import config
import os
import logging
import threading
import webbrowser
import time

def create_app(config_name='default'):
    """アプリケーションファクトリー"""
    app = Flask(__name__)
    
    # 設定読み込み
    app.config.from_object(config[config_name])
    
    # アプリケーションのルートディレクトリを取得
    app_root = os.path.dirname(os.path.abspath(__file__))
    
    # データベースパスを絶対パスに変更
    db_path = os.path.join(app_root, 'data', 'weather.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # データベース初期化
    db.init_app(app)
    
    # ブループリント登録
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # データベースとテーブル作成
    with app.app_context():
        # dataディレクトリの作成
        data_dir = os.path.join(app_root, 'data')
        os.makedirs(data_dir, exist_ok=True)
        db.create_all()
        
        # プリセット地域の追加
        from services.data_service import DataService
        from config import Config
        
        for preset in Config.PRESET_LOCATIONS:
            existing = DataService.get_location_by_name(preset['name'])
            if not existing:
                DataService.add_location(
                    name=preset['name'],
                    name_jp=preset['name_jp'],
                    lat=preset['lat'],
                    lon=preset['lon'],
                    country_code=preset.get('country_code', 'JP')
                )
                app.logger.info(f"プリセット地域を追加: {preset['name']}")
    
    return app

if __name__ == '__main__':
    # 開発サーバー起動
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)

    port = 5000

    # デバッグリロードによる二重起動を避けつつ、起動後にブラウザを開く
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        def _open_browser():
            url = f"http://127.0.0.1:{port}"
            # 少し待ってから開く（起動安定化）
            time.sleep(1.0)
            try:
                webbrowser.open(url)
            except Exception:
                pass

        threading.Thread(target=_open_browser, daemon=True).start()

    app.run(debug=True, host='0.0.0.0', port=port)
