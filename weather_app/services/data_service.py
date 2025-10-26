"""
データ管理サービス
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from models import db
from models.location import Location
from models.weather import WeatherForecast
import logging

logger = logging.getLogger(__name__)

class DataService:
    """データ管理サービス"""
    
    @staticmethod
    def get_all_locations() -> List[Location]:
        """全ての地域を取得"""
        return Location.query.all()
    
    @staticmethod
    def get_location_by_id(location_id: int) -> Optional[Location]:
        """IDで地域を取得"""
        return Location.query.get(location_id)
    
    @staticmethod
    def get_location_by_name(name: str) -> Optional[Location]:
        """名前で地域を取得"""
        return Location.query.filter_by(name=name).first()
    
    @staticmethod
    def add_location(name: str, name_jp: str = None, lat: float = None, 
                    lon: float = None, country_code: str = 'JP') -> Location:
        """
        地域を追加
        
        Args:
            name: 地域名
            name_jp: 日本語名
            lat: 緯度
            lon: 経度
            country_code: 国コード
            
        Returns:
            追加された地域
        """
        # 既存チェック
        existing = DataService.get_location_by_name(name)
        if existing:
            logger.warning(f"地域は既に存在します: {name}")
            return existing
        
        location = Location(
            name=name,
            name_jp=name_jp,
            lat=lat,
            lon=lon,
            country_code=country_code
        )
        db.session.add(location)
        db.session.commit()
        logger.info(f"地域を追加しました: {name}")
        return location
    
    @staticmethod
    def delete_location(location_id: int) -> bool:
        """
        地域を削除
        
        Args:
            location_id: 地域ID
            
        Returns:
            削除成功ならTrue
        """
        location = Location.query.get(location_id)
        if location:
            db.session.delete(location)
            db.session.commit()
            logger.info(f"地域を削除しました: {location.name}")
            return True
        return False
    
    @staticmethod
    def toggle_favorite(location_id: int) -> Optional[Location]:
        """
        お気に入りをトグル
        
        Args:
            location_id: 地域ID
            
        Returns:
            更新された地域
        """
        location = Location.query.get(location_id)
        if location:
            location.is_favorite = not location.is_favorite
            db.session.commit()
            logger.info(f"お気に入りを更新: {location.name} -> {location.is_favorite}")
            return location
        return None
    
    @staticmethod
    def save_weather_forecast(location_id: int, weather_data: Dict) -> WeatherForecast:
        """
        天気予報を保存
        
        Args:
            location_id: 地域ID
            weather_data: 天気データ
            
        Returns:
            保存された天気予報
        """
        # 既存データを削除（同じ日付のデータ）
        forecast_date = datetime.fromisoformat(weather_data['date'])
        WeatherForecast.query.filter_by(
            location_id=location_id,
            forecast_date=forecast_date
        ).delete()
        
        forecast = WeatherForecast(
            location_id=location_id,
            forecast_date=forecast_date,
            weather_main=weather_data.get('weather_main'),
            weather_description=weather_data.get('weather_description'),
            temp_max=weather_data.get('temp_max'),
            temp_min=weather_data.get('temp_min'),
            humidity=weather_data.get('humidity'),
            pressure=weather_data.get('pressure'),
            wind_speed=weather_data.get('wind_speed'),
            wind_deg=weather_data.get('wind_deg'),
            precipitation_probability=weather_data.get('precipitation_probability'),
            icon_code=weather_data.get('icon_code')
        )
        db.session.add(forecast)
        db.session.commit()
        logger.info(f"天気予報を保存しました: location_id={location_id}")
        return forecast
    
    @staticmethod
    def get_weather_forecast(location_id: int, date: datetime = None) -> Optional[WeatherForecast]:
        """
        天気予報を取得
        
        Args:
            location_id: 地域ID
            date: 予報日（Noneの場合は最新）
            
        Returns:
            天気予報
        """
        query = WeatherForecast.query.filter_by(location_id=location_id)
        if date:
            query = query.filter_by(forecast_date=date)
        return query.order_by(WeatherForecast.fetched_at.desc()).first()
    
    @staticmethod
    def get_weather_forecasts_by_locations(location_ids: List[int], date: datetime = None) -> List[Dict]:
        """
        複数地域の天気予報を取得
        
        Args:
            location_ids: 地域IDのリスト
            date: 予報日
            
        Returns:
            天気予報のリスト
        """
        results = []
        for location_id in location_ids:
            location = DataService.get_location_by_id(location_id)
            forecast = DataService.get_weather_forecast(location_id, date)
            
            if location and forecast:
                results.append({
                    'location': location.to_dict(),
                    'weather': forecast.to_dict()
                })
        
        return results
    
    @staticmethod
    def cleanup_old_forecasts(days: int = 7):
        """
        古い天気予報を削除
        
        Args:
            days: 保持日数
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = WeatherForecast.query.filter(
            WeatherForecast.fetched_at < cutoff_date
        ).delete()
        db.session.commit()
        logger.info(f"古い天気予報を削除しました: {deleted}件")
