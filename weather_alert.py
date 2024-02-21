import os
import requests
from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime, timezone, timedelta

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
opencage_api_key = os.getenv("OPENCAGE_API_KEY")

def get_coordinates(location):
	geocoding_url = f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={opencage_api_key}'
	response = requests.get(geocoding_url)
	data = response.json()

	if response.status_code == 200 and data['total_results'] > 0:
		lat = data['results'][0]['geometry']['lat']
		lon = data['results'][0]['geometry']['lng']
		return lat, lon
	else:
		print(f"Error {response.status_code}: {response.text}")
		return None

def get_weather(lat, lon):
	base_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&exclude=minutely,hourly,alerts&appid={openweather_api_key}'
	response = requests.get(base_url)

	if response.status_code == 200:
		return response.json()
	else:
		print(f"Error {response.status_code}: {response.text}")
		return None

def send_sms(message, to_number):
	client = Client(account_sid, auth_token)

	try:
		message = client.messages.create(
			from_=twilio_phone_number,
			body=message,
			to=to_number
		)
		print(f"Message sent successfully. SID: {message.sid}")
	except Exception as e:
		print(f"Error sending message: {e}")

def handle_incoming_sms(body, from_number):
	user_input = body.upper()
	coordinates = get_coordinates(user_input)

	if coordinates:
		lat, lon = coordinates
		weather_data = get_weather(lat, lon)

		if weather_data:
			current_weather = weather_data['current']
			daily_weather = weather_data['daily'][0]
			temperature = current_weather['temp']
			weather_description = current_weather['weather'][0]['description']

			response_message = f"{user_input}: \n"
			response_message += f"Weather: {weather_description}\n"
			response_message += f"Temperature: {temperature}°F\n"
			response_message += f"Feels Like: {current_weather['feels_like']}°F\n"
			response_message += f"Today's High: {daily_weather['temp']['max']}°F\n"
			response_message += f"Today's Low: {daily_weather['temp']['min']}°F\n"
			response_message += f"Humidity: {daily_weather['humidity']}%\n"
			response_message += f"Wind Speed: {daily_weather['wind_speed']} MPH\n"
			response_message += f"Sunrise: {timestamp_to_datetime(current_weather['sunrise'], is_sunrise=True)}\n"
			response_message += f"Sunset: {timestamp_to_datetime(current_weather['sunset'], is_sunrise=False)}\n"


			send_sms(response_message, from_number)

			return None
		else:
			return "Failed to retrieve weather data. Please try again later."
	else:
		return "Failed to retrieve coordinates. Please check your location and try again later."

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def receive_sms():
	body = request.values.get('Body', '')
	from_number = request.values.get('From', '')

	response_message = handle_incoming_sms(body, from_number)

	response = MessagingResponse()
	response.message(response_message)
	
	return str(response)

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
	app.run(debug=True)