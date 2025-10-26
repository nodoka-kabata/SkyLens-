"""
API エンドポイント
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from services.weather_service import WeatherService, WeatherAPIError
from services.data_service import DataService
from models.location import Location
from config import Config
import logging
import csv
import io

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api')

# WeatherServiceのインスタンス化
weather_service = WeatherService(
    api_key=Config.OPENWEATHER_API_KEY,
    base_url=Config.OPENWEATHER_BASE_URL,
    timeout=Config.API_TIMEOUT
)

@api_bp.route('/locations', methods=['GET'])
def get_locations():
    """全ての地域を取得"""
    try:
        locations = DataService.get_all_locations()
        return jsonify({
            'status': 'success',
            'data': [loc.to_dict() for loc in locations]
        }), 200
    except Exception as e:
        logger.error(f"地域取得エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/locations', methods=['POST'])
def add_location():
    """地域を追加"""
    try:
        data = request.get_json()
        name = data.get('name')
        name_jp = data.get('name_jp')
        lat = data.get('lat')
        lon = data.get('lon')
        country_code = data.get('country_code', 'JP')
        
        if not name:
            return jsonify({
                'status': 'error',
                'message': '地域名は必須です'
            }), 400
        
        location = DataService.add_location(name, name_jp, lat, lon, country_code)
        return jsonify({
            'status': 'success',
            'data': location.to_dict(),
            'message': '地域を追加しました'
        }), 201
    except Exception as e:
        logger.error(f"地域追加エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/locations/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """地域を削除"""
    try:
        success = DataService.delete_location(location_id)
        if success:
            return jsonify({
                'status': 'success',
                'message': '地域を削除しました'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': '地域が見つかりません'
            }), 404
    except Exception as e:
        logger.error(f"地域削除エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/locations/<int:location_id>/favorite', methods=['PUT'])
def toggle_favorite(location_id):
    """お気に入りをトグル"""
    try:
        location = DataService.toggle_favorite(location_id)
        if location:
            return jsonify({
                'status': 'success',
                'data': location.to_dict(),
                'message': 'お気に入りを更新しました'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': '地域が見つかりません'
            }), 404
    except Exception as e:
        logger.error(f"お気に入り更新エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/locations/search', methods=['GET'])
def search_locations():
    """地域を検索して座標を取得"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 5))
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': '検索クエリは必須です'
            }), 400
        
        # WeatherServiceで地域を検索
        results = weather_service.search_location(query, limit)
        
        return jsonify({
            'status': 'success',
            'data': results,
            'message': f'{len(results)}件の地域が見つかりました'
        }), 200
        
    except WeatherAPIError as e:
        logger.error(f"地域検索エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/weather/forecast', methods=['GET'])
def get_weather_forecast():
    """天気予報を取得"""
    try:
        location_ids_str = request.args.get('location_ids', '')
        date_str = request.args.get('date')
        
        if not location_ids_str:
            return jsonify({
                'status': 'error',
                'message': '地域IDは必須です'
            }), 400
        
        location_ids = [int(id.strip()) for id in location_ids_str.split(',')]
        
        # 日付パース
        forecast_date = None
        if date_str:
            forecast_date = datetime.fromisoformat(date_str)
        
        forecasts = DataService.get_weather_forecasts_by_locations(location_ids, forecast_date)
        
        return jsonify({
            'status': 'success',
            'data': {'forecasts': forecasts}
        }), 200
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': '無効な地域IDまたは日付形式です'
        }), 400
    except Exception as e:
        logger.error(f"天気予報取得エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/weather/refresh', methods=['POST'])
def refresh_weather():
    """天気データを更新"""
    try:
        data = request.get_json()
        location_ids = data.get('location_ids', [])
        
        if not location_ids:
            return jsonify({
                'status': 'error',
                'message': '地域IDは必須です'
            }), 400
        
        results = []
        errors = []
        
        for location_id in location_ids:
            try:
                location = DataService.get_location_by_id(location_id)
                if not location:
                    errors.append(f"地域ID {location_id} が見つかりません")
                    continue
                
                # 天気データを取得
                weather_data = weather_service.get_tomorrow_forecast(
                    location.name, 
                    location.country_code
                )
                
                # データベースに保存
                forecast = DataService.save_weather_forecast(location_id, weather_data)
                
                results.append({
                    'location': location.to_dict(),
                    'weather': forecast.to_dict()
                })
            except WeatherAPIError as e:
                errors.append(f"{location.name}: {str(e)}")
            except Exception as e:
                logger.error(f"天気データ更新エラー (location_id={location_id}): {e}")
                errors.append(f"地域ID {location_id}: {str(e)}")
        
        response = {
            'status': 'success' if results else 'error',
            'data': {'forecasts': results}
        }
        
        if errors:
            response['errors'] = errors
            response['message'] = f"{len(results)}件成功、{len(errors)}件失敗"
        else:
            response['message'] = f"{len(results)}件の天気データを更新しました"
        
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"天気データ更新エラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/weather/export', methods=['GET'])
def export_weather():
    """天気データをエクスポート"""
    try:
        format_type = request.args.get('format', 'csv')
        location_ids_str = request.args.get('location_ids', '')
        date_str = request.args.get('date')
        
        if not location_ids_str:
            return jsonify({
                'status': 'error',
                'message': '地域IDは必須です'
            }), 400
        
        location_ids = [int(id.strip()) for id in location_ids_str.split(',')]
        
        # 日付パース
        forecast_date = None
        if date_str:
            forecast_date = datetime.fromisoformat(date_str)
        
        forecasts = DataService.get_weather_forecasts_by_locations(location_ids, forecast_date)
        
        if format_type == 'csv':
            # CSV形式でエクスポート
            output = io.StringIO()
            writer = csv.writer(output)
            
            # ヘッダー
            writer.writerow([
                '地域名', '日本語名', '日付', '天気', '天気詳細',
                '最高気温(℃)', '最低気温(℃)', '湿度(%)', '気圧(hPa)',
                '風速(m/s)', '風向(度)', '降水確率(%)'
            ])
            
            # データ
            for item in forecasts:
                loc = item['location']
                weather = item['weather']
                writer.writerow([
                    loc['name'], loc['name_jp'], weather['forecast_date'],
                    weather['weather_main'], weather['weather_description'],
                    weather['temp_max'], weather['temp_min'],
                    weather['humidity'], weather['pressure'],
                    weather['wind_speed'], weather['wind_deg'],
                    weather['precipitation_probability']
                ])
            
            output.seek(0)
            filename = f"weather_forecast_{datetime.now().strftime('%Y%m%d')}.csv"
            
            from flask import make_response
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        
        elif format_type == 'json':
            # JSON形式でエクスポート
            return jsonify({
                'status': 'success',
                'data': {'forecasts': forecasts}
            }), 200
        
        else:
            return jsonify({
                'status': 'error',
                'message': 'サポートされていない形式です'
            }), 400
            
    except Exception as e:
        logger.error(f"エクスポートエラー: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
