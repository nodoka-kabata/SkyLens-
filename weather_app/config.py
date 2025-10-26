"""
アプリケーション設定
"""
import os
from dotenv import load_dotenv

# .envファイル読み込み
load_dotenv()

class Config:
    """基本設定"""
    # Flask設定
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data/weather.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenWeatherMap API設定
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    # アプリケーション設定
    MAX_LOCATIONS = 10
    API_TIMEOUT = 10
    CACHE_DURATION = 1800  # 30分
    
    # 日本の主要都市プリセット
    PRESET_LOCATIONS = [
        {'name': 'Tokyo', 'name_jp': '東京', 'lat': 35.6762, 'lon': 139.6503, 'country_code': 'JP'},
        {'name': 'Osaka', 'name_jp': '大阪', 'lat': 34.6937, 'lon': 135.5023, 'country_code': 'JP'},
        {'name': 'Nagoya', 'name_jp': '名古屋', 'lat': 35.1815, 'lon': 136.9066, 'country_code': 'JP'},
        {'name': 'Sapporo', 'name_jp': '札幌', 'lat': 43.0642, 'lon': 141.3469, 'country_code': 'JP'},
        {'name': 'Fukuoka', 'name_jp': '福岡', 'lat': 33.5904, 'lon': 130.4017, 'country_code': 'JP'},
        {'name': 'Sendai', 'name_jp': '仙台', 'lat': 38.2682, 'lon': 140.8694, 'country_code': 'JP'},
        {'name': 'Hiroshima', 'name_jp': '広島', 'lat': 34.3853, 'lon': 132.4553, 'country_code': 'JP'},
        {'name': 'Kyoto', 'name_jp': '京都', 'lat': 35.0116, 'lon': 135.7681, 'country_code': 'JP'},
    ]

class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True

class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False

# 環境に応じた設定を取得
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
