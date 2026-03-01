from flask import Flask, render_template, request
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        # Follow instructions in README.md to get your API key
        api_key = "PLACE_YOUR_API_KEY_HERE"
        
        city = request.form.get('city')
        lat = request.form.get('lat')
        lon = request.form.get('lon')

        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        else:
            url = None

        if url:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data.get('name', 'Unknown Location'),
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'].capitalize(),
                    'humidity': data['main']['humidity']
                }
            else:
                error_message = "Location not found. Please try again!"

    return render_template('index.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)