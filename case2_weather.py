import requests
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

def get_coords(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'WeatherApp/1.0'})
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            st.error(f"City '{city_name}' not found.")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error in geocoding request: {str(e)}")
        return None, None

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max&timezone=auto&forecast_days=7"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "daily" in data:
            return data["daily"]
        else:
            st.error("Weather forecast does not contain daily data.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error in weather forecast request: {str(e)}")
        return None

def run_case2():
    st.header("Weather Forecast for 7 Days (Case 2)")

    city = st.text_input("Enter city name (in English)", "Almaty")

    if not city:
        st.warning("Please enter a city name.")
        return

    lat, lon = get_coords(city)
    if lat is None or lon is None:
        st.error("City not found or unavailable. Try another city.")
        return

    forecast = get_weather(lat, lon)
    if not forecast:
        st.error("Unable to retrieve weather forecast. Check your network connection.")
        return

    days = []
    temps = []

    for i, temp in enumerate(forecast['temperature_2m_max']):
        dt = datetime.strptime(forecast['time'][i], '%Y-%m-%d').strftime('%d %b')
        days.append(dt)
        temps.append(temp)

    avg_temp = sum(temps) / len(temps)
    min_temp = min(temps)
    max_temp = max(temps)

    st.subheader(f"Forecast for: {city.title()}")
    st.write(f"Average temperature: {avg_temp:.1f}°C")
    st.write(f"Minimum: {min_temp:.1f}°C, Maximum: {max_temp:.1f}°C")

    st.subheader("Temperature by Day")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(days, temps, marker='o', color='teal', linewidth=2)
    ax.set_title("7-Day Temperature Forecast", fontsize=16)
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True)

    for i, temp in enumerate(temps):
        ax.text(i, temp + 0.5, f"{temp:.1f}°", ha='center', fontsize=9)

    st.pyplot(fig)

if __name__ == "__main__":
    run_case2()