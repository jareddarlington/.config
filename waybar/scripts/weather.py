import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
# .env file should have format "WEATHER_API_KEY=KEY"
load_dotenv()

# Fetch the API key from the environment
API_KEY = os.getenv("WEATHER_API_KEY")

# Base URL for the WeatherAPI current weather endpoint
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Location for the weather query
LOCATION = "Seattle"

# Weather icons
weather_icons = {
    "Sunny": "",
    "Clear": "󰖔",
    "Partly cloudy": "󰖐",
    "Cloudy": "󰖐",
    "Overcast": "󰖐",
    "Mist": "",
    "Light drizzle": "",
    "Light rain": "",
    "Moderate rain": "",
    "Heavy rain": "",
    "Fog": "",
    "Patchy light snow": "",
    "Light snow": "",
    "Patchy moderate snow": "",
    "Moderate snow": "",
    "Patchy heavy snow": "",
    "Heavy snow": "",
    "default": "",
}


def get_current_weather(api_key, location):
    try:
        # Build the query URL
        url = f"{BASE_URL}?key={api_key}&q={location}"

        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the JSON response
        data = response.json()
        current_temp = data["current"]["temp_f"]  # Temperature in Fahrenheit
        current_condition = data["current"]["condition"]["text"]  # Weather condition

        icon = weather_icons[current_condition] if current_condition in weather_icons else weather_icons["default"]

        return current_temp, current_condition, icon

    except requests.exceptions.RequestException as e:
        return None, None, f"Error fetching weather data: {e}"


# Fetch and print the current weather data in Seattle
if __name__ == "__main__":
    if not API_KEY:
        out_data = {
            "text": "Error",
            "alt": "API key missing",
            "tooltip": "API key missing",
            "class": "ERROR",
        }
    else:
        temp, status, icon = get_current_weather(API_KEY, LOCATION)

        if temp is None:
            # Handle error
            out_data = {
                "text": "Error",
                "alt": "Error fetching weather data",
                "tooltip": "Error fetching weather data",
                "class": "ERROR",
            }
        else:
            # Format tooltip text for Waybar
            tooltip_text = str.format(
                "{}\n{}",
                f'<span size="x-large">{temp:.0f}°</span>',
                f"<big>{status}</big>",
            )

            # Waybar module output data
            out_data = {
                "text": f"{temp:.0f}°",  # Display icon and temperature
                "alt": status,  # Weather condition text
                "tooltip": tooltip_text,  # Full tooltip with additional data
                "class": status,  # Needed for coloring by waybar style
            }

# Print Waybar JSON output
print(json.dumps(out_data))
