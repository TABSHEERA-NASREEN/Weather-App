from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        api_key = "c899243db695480cb8ee58d4c418e6ef"  # Replace with your OpenWeather API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            weather_data = {"error": "City not found"}

    return render_template("index.html", weather_data=weather_data)

@app.route("/forecast", methods=["POST"])
def forecast():
    city = request.form.get("city")
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    forecast_data = []
    if response.status_code == 200:
        data = response.json()
        for i in range(0, 40, 8):  # 5 days (8 intervals per day)
            day_data = data["list"][i]
            forecast_data.append({
                "date": day_data["dt_txt"],
                "temp": day_data["main"]["temp"],
                "description": day_data["weather"][0]["description"],
                "icon": day_data["weather"][0]["icon"],
            })

    return render_template("forecast.html", forecast_data=forecast_data)


if __name__ == "__main__":
    app.run(debug=True)
