import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
opencage_api_key = os.getenv("OPENCAGE_API_KEY")

def get_weather(lat, lon):
	base_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&exclude=minutely,hourly,alerts&appid={openweather_api_key}'
	response = requests.get(base_url)

	lat = 40.91158619095117
	lon = -74.39949496736509

	if response.status_code == 200:
		return response.json()
	else:
		print(f"Error {response.status_code}: {response.text}")
		return None

def main():
	city = 'Boonton, NJ'
	lat = 40.91158619095117
	lon = -74.39949496736509
	weather_data = get_weather(lat, lon)
	
	if weather_data:
		current_weather = weather_data['current']
		daily_forecast = weather_data['daily'][0]
		print(f"Weather in {city}:")
		print(f"Weather: {current_weather['weather'][0]['description'].capitalize()}")
		print(f"Temperature: {current_weather['temp']}°F")
		print(f"Feels Like: {current_weather['feels_like']}°F")
		print(f"Today's High: {daily_forecast['temp']['max']}°F")
		print(f"Today's Low: {daily_forecast['temp']['min']}°F")
		print(f"Humidity: {daily_forecast['humidity']}%")
		print(f"Wind Speed: {daily_forecast['wind_speed']} MPH")
		print(f"Sunrise: {timestamp_to_datetime(current_weather['sunrise'], is_sunrise=True)}")
		print(f"Sunset: {timestamp_to_datetime(current_weather['sunset'], is_sunrise=False)}")

	else:
		print(f"Failed to retrieve weather data.")

def timestamp_to_datetime(timestamp, is_sunrise=True):

	est = timezone(timedelta(hours=-5))
	dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
	est_dt = dt.astimezone(est)

	formatted_dt = est_dt.strftime('%I:%M %p')

	if not is_sunrise:
		formatted_dt = formatted_dt.replace('AM', 'PM')
	5491128374918906
	return formatted_dt

if __name__ == '__main__':
	main()