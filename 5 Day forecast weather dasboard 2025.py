import requests
import tkinter as tk
from tkinter import messagebox

# Replace with your actual OpenWeatherMap API key
API_KEY = ""

# API Endpoints
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Get coordinates based on city input
def get_coordinates(city, state="", country="US", limit=1):
    params = {
        "q": f"{city},{state},{country}",
        "limit": limit,
        "appid": API_KEY
    }
    response = requests.get(GEO_URL, params=params)
    response.raise_for_status()
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    else:
        raise ValueError("City not found!")

# Get both current weather and 5-day forecast
def get_weather_data(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "imperial"
    }

    current = requests.get(WEATHER_URL, params=params).json()
    forecast = requests.get(FORECAST_URL, params=params).json()

    return current, forecast

# Display weather data in the GUI
def display_weather():
    city = city_entry.get()
    state = state_entry.get()
    country = country_entry.get() or "US"

    try:
        lat, lon = get_coordinates(city, state, country)
        current, forecast = get_weather_data(lat, lon)

        # Clear previous output
        output_text.delete("1.0", tk.END)

        # Display current weather
        name = current["name"]
        weather = current["weather"][0]["description"].title()
        temp = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        wind = current["wind"]["speed"]

        output_text.insert(tk.END, f"Weather in {name}\n")
        output_text.insert(tk.END, f"Condition: {weather}\n")
        output_text.insert(tk.END, f"Temperature: {temp}°F\n")
        output_text.insert(tk.END, f"Humidity: {humidity}%\n")
        output_text.insert(tk.END, f"Wind Speed: {wind} mph\n\n")

        # Display filtered 5-day forecast (daily at noon)
        output_text.insert(tk.END, "5-Day Forecast (Daily at Noon):\n")
        printed_days = 0
        for entry in forecast["list"]:
            if "12:00:00" in entry["dt_txt"]:
                dt = entry["dt_txt"].split()[0]
                f_temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"].title()
                output_text.insert(tk.END, f"{dt} | {f_temp}°F | {desc}\n")
                printed_days += 1
                if printed_days == 5:
                    break

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# GUI Layout
root = tk.Tk()
root.title("Weather Dashboard")

# Input fields
tk.Label(root, text="City:").grid(row=0, column=0)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1)

tk.Label(root, text="State (opt):").grid(row=1, column=0)
state_entry = tk.Entry(root)
state_entry.grid(row=1, column=1)

tk.Label(root, text="Country (default US):").grid(row=2, column=0)
country_entry = tk.Entry(root)
country_entry.grid(row=2, column=1)

# Button
get_btn = tk.Button(root, text="Get Weather", command=display_weather)
get_btn.grid(row=3, columnspan=2, pady=10)

# Output display
output_text = tk.Text(root, height=20, width=60)
output_text.grid(row=4, column=0, columnspan=2)

root.mainloop()

