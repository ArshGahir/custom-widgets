from flask import Flask, jsonify, request
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

app = Flask(__name__)

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Route to get weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    # Get the latitude and longitude from query parameters
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    days = request.args.get('days', type=int, default=3)

    if not latitude or not longitude or not days:
        return jsonify({'error': 'No coordinates or days provided'}), 400

    # Setup parameters for Open-Meteo API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "hourly": "temperature_2m",
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"],
        "timezone": "America/New_York",
        "forecast_days": days
    }

    url = "https://api.open-meteo.com/v1/forecast"

    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    # Extract current weather data
    current = response.Current()
    current_data = {
        "temperature_2m": current.Variables(0).Value(),
        "relative_humidity_2m": current.Variables(1).Value(),
        "apparent_temperature": current.Variables(2).Value(),
        "is_day": current.Variables(3).Value(),
        "precipitation": current.Variables(4).Value(),
        "rain": current.Variables(5).Value(),
        "showers": current.Variables(6).Value(),
        "snowfall": current.Variables(7).Value(),
        "weather_code": current.Variables(8).Value(),
        "cloud_cover": current.Variables(9).Value(),
        "wind_speed_10m": current.Variables(10).Value(),
        "wind_direction_10m": current.Variables(11).Value(),
        "wind_gusts_10m": current.Variables(12).Value(),
    }

    # Extract hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).tolist(),
        "temperature_2m": hourly_temperature_2m.tolist() if hasattr(hourly_temperature_2m, 'tolist') else hourly_temperature_2m
    }

    # Extract daily data
    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ).tolist(),
        "weather_code": daily.Variables(0).ValuesAsNumpy().tolist() if hasattr(daily.Variables(0).ValuesAsNumpy(), 'tolist') else daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_max": daily.Variables(1).ValuesAsNumpy().tolist() if hasattr(daily.Variables(1).ValuesAsNumpy(), 'tolist') else daily.Variables(1).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(2).ValuesAsNumpy().tolist() if hasattr(daily.Variables(2).ValuesAsNumpy(), 'tolist') else daily.Variables(2).ValuesAsNumpy(),
        "apparent_temperature_max": daily.Variables(3).ValuesAsNumpy().tolist() if hasattr(daily.Variables(3).ValuesAsNumpy(), 'tolist') else daily.Variables(3).ValuesAsNumpy(),
        "apparent_temperature_min": daily.Variables(4).ValuesAsNumpy().tolist() if hasattr(daily.Variables(4).ValuesAsNumpy(), 'tolist') else daily.Variables(4).ValuesAsNumpy(),
        "sunrise": daily.Variables(5).ValuesAsNumpy().tolist() if hasattr(daily.Variables(5).ValuesAsNumpy(), 'tolist') else daily.Variables(5).ValuesAsNumpy(),
        "sunset": daily.Variables(6).ValuesAsNumpy().tolist() if hasattr(daily.Variables(6).ValuesAsNumpy(), 'tolist') else daily.Variables(6).ValuesAsNumpy(),
        "daylight_duration": daily.Variables(7).ValuesAsNumpy().tolist() if hasattr(daily.Variables(7).ValuesAsNumpy(), 'tolist') else daily.Variables(7).ValuesAsNumpy(),
        "sunshine_duration": daily.Variables(8).ValuesAsNumpy().tolist() if hasattr(daily.Variables(8).ValuesAsNumpy(), 'tolist') else daily.Variables(8).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(9).ValuesAsNumpy().tolist() if hasattr(daily.Variables(9).ValuesAsNumpy(), 'tolist') else daily.Variables(9).ValuesAsNumpy(),
        "rain_sum": daily.Variables(10).ValuesAsNumpy().tolist() if hasattr(daily.Variables(10).ValuesAsNumpy(), 'tolist') else daily.Variables(10).ValuesAsNumpy(),
        "showers_sum": daily.Variables(11).ValuesAsNumpy().tolist() if hasattr(daily.Variables(11).ValuesAsNumpy(), 'tolist') else daily.Variables(11).ValuesAsNumpy(),
        "snowfall_sum": daily.Variables(12).ValuesAsNumpy().tolist() if hasattr(daily.Variables(12).ValuesAsNumpy(), 'tolist') else daily.Variables(12).ValuesAsNumpy(),
        "precipitation_hours": daily.Variables(13).ValuesAsNumpy().tolist() if hasattr(daily.Variables(13).ValuesAsNumpy(), 'tolist') else daily.Variables(13).ValuesAsNumpy(),
        "precipitation_probability_max": daily.Variables(14).ValuesAsNumpy().tolist() if hasattr(daily.Variables(14).ValuesAsNumpy(), 'tolist') else daily.Variables(14).ValuesAsNumpy(),
        "wind_speed_10m_max": daily.Variables(15).ValuesAsNumpy().tolist() if hasattr(daily.Variables(15).ValuesAsNumpy(), 'tolist') else daily.Variables(15).ValuesAsNumpy(),
        "wind_gusts_10m_max": daily.Variables(16).ValuesAsNumpy().tolist() if hasattr(daily.Variables(16).ValuesAsNumpy(), 'tolist') else daily.Variables(16).ValuesAsNumpy(),
        "wind_direction_10m_dominant": daily.Variables(17).ValuesAsNumpy().tolist() if hasattr(daily.Variables(17).ValuesAsNumpy(), 'tolist') else daily.Variables(17).ValuesAsNumpy(),
    }

    return jsonify({
        "current": current_data,
        "hourly": hourly_data,
        "daily": daily_data
    })

if __name__ == '__main__':
    app.run(debug=True)
