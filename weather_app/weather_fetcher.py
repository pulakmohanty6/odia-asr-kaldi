import requests
from datetime import datetime, timedelta

API_KEY = "bf8cb89eb3c74c5804e08d5f818cf3bf" 

def fetch_weather_data(city_name, intent, time_frame):
    """
    Fetches live weather from OpenWeatherMap and extracts specific metrics.
    """
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{city_name},IN",  # Restrict search to India
        "appid": API_KEY,
        "units": "metric"        # Get temperature in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return f"Error: Cannot find weather data for {city_name}."
        
        data = response.json()
        
        # Determine target date string (YYYY-MM-DD)
        target_date = datetime.now()
        if time_frame == "tomorrow":
            target_date += timedelta(days=1)
        target_date_str = target_date.strftime("%Y-%m-%d")

        # Filter the 3-hour forecasts to find entries matching our target date
        day_forecasts = [
            item for item in data["list"] 
            if item["dt_txt"].startswith(target_date_str)
        ]

        if not day_forecasts:
            return "Error: No forecast data found for that time frame."

        # Extract relevant metrics across the day
        temps = [item["main"]["temp"] for item in day_forecasts]
        avg_temp = round(sum(temps) / len(temps), 1)
        
        # Check if any 3-hour slot predicts rain/storms
        weather_conditions = [item["weather"][0]["main"].lower() for item in day_forecasts]
        has_rain = any(any(k in cond for k in ["rain", "drizzle", "thunderstorm"]) for cond in weather_conditions)

        # Structure the text response based on user intent
        time_word = "ଆଜି" if time_frame == "today" else "ଆସନ୍ତାକାଲି"
        
        if intent == "temperature":
            return f"{time_word} {city_name}ର ହାରาହାରି ତାପମାତ୍ରା ପ୍ରାୟ {avg_temp} ଡିଗ୍ରୀ ସେଲସିୟସ ରହିବ।"
        
        elif intent == "rain":
            if has_rain:
                return f"ହଁ, {time_word} {city_name}ରେ ବର୍ଷା ହେବାର ସମ୍ଭାବନା ଅଛି।"
            else:
                return f"ନା, {time_word} {city_name}ରେ ବର୍ଷା ହେବାର ସମ୍ଭାବନା ନାହିଁ, ପାଗ ସଫା ରହିବ।"
        
        else: # General summary intent
            rain_status = "ବର୍ଷା ହୋଇପାରେ" if has_rain else "ପାଗ ସଫା ରହିବ"
            return f"{time_word} {city_name}ର ତାପମାତ୍ରା {avg_temp} ଡିଗ୍ରୀ ରହିବ ଏବଂ {rain_status}।"

    except Exception as e:
        return "Error: ଦୁଃଖିତ, ସର୍ଭର ସହିତ ସଂଯୋଗ ହୋଇପାରିଲା ନାହିଁ।"

if __name__ == "__main__":
    print(fetch_weather_data("Bhubaneswar", "rain", "today"))