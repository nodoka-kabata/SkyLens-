"""
OpenWeatherMap API連携サービス
"""
import requests
from datetime import datetime, timedelta, time
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class WeatherAPIError(Exception):
    """天気APIエラー"""
    pass

class WeatherService:
    """天気データ取得サービス"""
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 10):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.geo_url = "http://api.openweathermap.org/geo/1.0"
    
    def get_tomorrow_forecast(self, location_name: str, country_code: str = 'JP') -> Optional[Dict]:
        """
        明日の天気予報を取得
        
        Args:
            location_name: 地域名
            country_code: 国コード
            
        Returns:
            天気予報データ、エラー時はNone
        """
        try:
            # APIエンドポイント
            url = f"{self.base_url}/forecast"
            
            # リクエストパラメータ
            params = {
                'q': f"{location_name},{country_code}",
                'appid': self.api_key,
                'units': 'metric',  # 摂氏
                'lang': 'ja',       # 日本語
                # 明日の全時間帯が確実に含まれるように十分な件数を取得（最大40件=5日分）
                'cnt': 40
            }
            
            logger.info(f"天気データを取得中: {location_name}")
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # 明日のデータを抽出
            tomorrow_data = self._extract_tomorrow_data(data)
            
            return tomorrow_data
            
        except requests.exceptions.Timeout:
            logger.error(f"APIタイムアウト: {location_name}")
            raise WeatherAPIError("APIタイムアウトが発生しました")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("APIキーが無効です")
                raise WeatherAPIError("APIキーが無効です")
            elif e.response.status_code == 404:
                logger.error(f"地域が見つかりません: {location_name}")
                raise WeatherAPIError(f"地域が見つかりません: {location_name}")
            elif e.response.status_code == 429:
                logger.error("API制限に達しました")
                raise WeatherAPIError("API制限に達しました。しばらく待ってから再試行してください")
            else:
                logger.error(f"APIエラー: {e}")
                raise WeatherAPIError(f"APIエラーが発生しました: {e}")
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            raise WeatherAPIError(f"予期しないエラーが発生しました: {e}")
    
    def _extract_tomorrow_data(self, api_response: Dict) -> Dict:
        """
        APIレスポンスから明日のデータを抽出
        
        Args:
            api_response: OpenWeatherMap APIレスポンス
            
        Returns:
            明日の天気データ
        """
        # タイムゾーンオフセット（秒）: 都市ローカル時刻に変換するために使用
        tz_offset_sec = api_response.get('city', {}).get('timezone', 0) or 0

        # 「明日」のローカル日付を算出
        now_local = datetime.utcnow() + timedelta(seconds=tz_offset_sec)
        tomorrow_date = (now_local + timedelta(days=1)).date()
        
        # 明日のデータをフィルタリング
        tomorrow_forecasts = []
        for item in api_response.get('list', []):
            dt_local = datetime.utcfromtimestamp(item['dt']) + timedelta(seconds=tz_offset_sec)
            if dt_local.date() == tomorrow_date:
                # 以降の代表選定で使うためローカル時刻も添えて保持
                enriched = dict(item)
                enriched['_dt_local'] = dt_local
                tomorrow_forecasts.append(enriched)
        
        if not tomorrow_forecasts:
            # データがない場合は最初のデータを使用
            tomorrow_forecasts = api_response.get('list', [])[:1]
        
        # 代表的なデータを選択（正午に最も近いローカル時刻のデータ）
        if tomorrow_forecasts:
            noon_local = datetime.combine(tomorrow_date, time(12, 0))
            representative_data = min(
                tomorrow_forecasts,
                key=lambda x: abs((x.get('_dt_local') or noon_local) - noon_local)
            )
        else:
            representative_data = {}
        
        # 最高・最低気温を計算（明日の全時間帯から）
        if tomorrow_forecasts:
            # 各時間帯のスロット最大/最小を使って日合成の最大/最小を算出
            slot_maxes = [
                item.get('main', {}).get('temp_max', item.get('main', {}).get('temp'))
                for item in tomorrow_forecasts
                if item.get('main') is not None
            ]
            slot_mins = [
                item.get('main', {}).get('temp_min', item.get('main', {}).get('temp'))
                for item in tomorrow_forecasts
                if item.get('main') is not None
            ]
            # フォールバック: 配列が空なら代表データの値を使う
            temp_max = max(slot_maxes) if slot_maxes else representative_data.get('main', {}).get('temp', 0)
            temp_min = min(slot_mins) if slot_mins else representative_data.get('main', {}).get('temp', 0)
        else:
            # データがない場合はデフォルト値
            temp_max = representative_data.get('main', {}).get('temp', 0)
            temp_min = representative_data.get('main', {}).get('temp', 0)
        
        # 降水確率の平均
        pops = [item.get('pop', 0) * 100 for item in tomorrow_forecasts]
        avg_pop = int(sum(pops) / len(pops)) if pops else 0
        
        weather_info = representative_data.get('weather', [{}])[0]
        
        return {
            'date': tomorrow_date.isoformat(),
            'weather_main': weather_info.get('main', ''),
            'weather_description': weather_info.get('description', ''),
            'temp_max': round(temp_max, 1),
            'temp_min': round(temp_min, 1),
            'humidity': representative_data.get('main', {}).get('humidity', 0),
            'pressure': representative_data.get('main', {}).get('pressure', 0),
            'wind_speed': representative_data.get('wind', {}).get('speed', 0),
            'wind_deg': representative_data.get('wind', {}).get('deg', 0),
            'precipitation_probability': avg_pop,
            'icon_code': weather_info.get('icon', '01d')
        }
    
    def search_location(self, query: str, limit: int = 5) -> List[Dict]:
        """
        地域名で検索して座標を取得
        
        Args:
            query: 検索クエリ（都市名）
            limit: 取得件数
            
        Returns:
            検索結果のリスト
        """
        try:
            url = f"{self.geo_url}/direct"
            params = {
                'q': query,
                'limit': limit,
                'appid': self.api_key
            }
            
            logger.info(f"地域を検索中: {query}")
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            results = response.json()
            
            # 結果を整形
            formatted_results = []
            for item in results:
                formatted_results.append({
                    'name': item.get('name', ''),
                    'local_names': item.get('local_names', {}),
                    'lat': item.get('lat'),
                    'lon': item.get('lon'),
                    'country': item.get('country', ''),
                    'state': item.get('state', '')
                })
            
            return formatted_results
            
        except requests.exceptions.Timeout:
            logger.error(f"検索タイムアウト: {query}")
            raise WeatherAPIError("検索タイムアウトが発生しました")
        except requests.exceptions.HTTPError as e:
            logger.error(f"検索APIエラー: {e}")
            raise WeatherAPIError(f"検索エラーが発生しました: {e}")
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            raise WeatherAPIError(f"予期しないエラーが発生しました: {e}")
