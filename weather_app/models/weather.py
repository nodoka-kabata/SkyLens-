"""
天気予報データモデル
"""
from datetime import datetime
from models import db

class WeatherForecast(db.Model):
    """天気予報情報"""
    __tablename__ = 'weather_forecasts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    forecast_date = db.Column(db.DateTime, nullable=False)
    weather_main = db.Column(db.String(50))
    weather_description = db.Column(db.String(100))
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)
    wind_deg = db.Column(db.Integer)
    precipitation_probability = db.Column(db.Integer)
    icon_code = db.Column(db.String(10))
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # インデックス
    __table_args__ = (
        db.Index('idx_location_date', 'location_id', 'forecast_date'),
    )
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'location_id': self.location_id,
            'forecast_date': self.forecast_date.isoformat() if self.forecast_date else None,
            'weather_main': self.weather_main,
            'weather_description': self.weather_description,
            'temp_max': self.temp_max,
            'temp_min': self.temp_min,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'precipitation_probability': self.precipitation_probability,
            'icon_code': self.icon_code,
            'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None
        }
    
    def __repr__(self):
        return f'<WeatherForecast location_id={self.location_id} date={self.forecast_date}>'
