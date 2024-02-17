# Weather SMS App

This is a simple Weather SMS app built in Python using Flask, Twilio, OpenCage Geocoding API, and OpenWeatherMap API.

## Getting Started

### Prerequisites

- Twilio Account
- OpenWeatherMap Account
- OpenCage Geocoding Account

Make sure you have the following installed:

- Python 3.x
- `pip` (Python package installer)
- gunicorn (for local testing with Twilio)

### Clone the Repository

Clone the repositroy to your local machine using the following command:

	git clone https://github.com/kmparks60/weather_alert.git

### Install Dependencies

Navigate to the project directory and install the required dependencies:

	cd weather_alert
	pip install -r required.txt

### Run the Flask Application Locally

In two separate tabs run the following code:

	python weather_alert.py --port 5000
		or
	python3 weather_alert.py --port 5000

The Flask app will be running at `http://127.0.0.1:5000/`. Use Ngrok to expose this local server to the internet for Twilio webhook configuration.

	ngrok http 5000

### Twilio Configuration

1. Log in to your Twilio account.
2. Navigate to the "Phone Numbers" section.
3. Click your toll-free number you would like to use.
4. Scroll down to "A Message Comes In" webhook URL to point your Ngrok or deployment URL with '/sms' endpoint (e.g., `https://abc123.ngrok.io/sms`).

### Usage

1. Send an SMS to your Twilio phone number with the location information(city, state or ZIP code.)
2. Twilio will forward the message to your Flask app.
3. Your Flask app will respond with the current weather information.

### If you'd like to contribute, please fork the repository, create a new branch, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.