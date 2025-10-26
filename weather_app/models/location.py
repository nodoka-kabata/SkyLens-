"""
地域データモデル
"""
from datetime import datetime
from models import db

class Location(db.Model):
    """地域情報"""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    name_jp = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    country_code = db.Column(db.String(2))
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション
    weather_forecasts = db.relationship('WeatherForecast', backref='location', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'name': self.name,
            'name_jp': self.name_jp,
            'lat': self.lat,
            'lon': self.lon,
            'country_code': self.country_code,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Location {self.name}>'
