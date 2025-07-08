import requests
import matplotlib.pyplot as plt
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

# Set Matplotlib font to avoid glyph warnings
plt.rcParams['font.family'] = 'DejaVu Sans'  # Replace with 'Noto Sans' if installed

def scrape_gasoline_prices():
    url = "https://www.globalpetrolprices.com/gasoline_prices/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with gasoline prices
        table = soup.find('table', id='graphic')
        if not table:
            st.error("Could not find price table on the website.")
            return None
        
        # Extract data
        countries = []
        prices = []
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                country = cols[0].text.strip()
                price_text = cols[1].text.strip()
                try:
                    price = float(price_text.replace(',', ''))  # Convert to float
                    countries.append(country)
                    prices.append(price)
                except ValueError:
                    continue
        
        return pd.DataFrame({'Country': countries, 'Price (USD/L)': prices})
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def run_case1():
    st.header("Gasoline Prices by Country (Case 1)")

    # Selected countries for display (mix of high, low, and Kazakhstan)
    selected_countries = [
        "Norway", "Netherlands", "Germany", "United States", "Kazakhstan",
        "Malaysia", "Venezuela", "Iran"
    ]

    # Fetch real-time data
    st.subheader("Fetching Data")
    df = scrape_gasoline_prices()
    if df is None:
        st.error("Unable to retrieve gasoline prices. Check your internet connection or try again later.")
        return

    # Filter for selected countries
    df_filtered = df[df['Country'].isin(selected_countries)]
    if df_filtered.empty:
        st.error("No data available for the selected countries.")
        return

    countries = df_filtered['Country'].tolist()
    prices = df_filtered['Price (USD/L)'].tolist()

    # Display data table
    st.subheader("Data (USD per Liter)")
    st.dataframe(df_filtered.set_index('Country'))

    # Plot bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(countries, prices, color='skyblue')

    # Highlight Kazakhstan
    for i, country in enumerate(countries):
        if country == "Kazakhstan":
            bars[i].set_color("orange")
            ax.text(i, prices[i] + 0.05, "KZ", ha='center')

    ax.set_title("Gasoline Prices by Country", fontsize=16)
    ax.set_ylabel("Price (USD/L)")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig)

    # Analytics
    st.subheader("Analytics")
    st.write(f"Maximum: **{max(prices):.2f} USD/L** — {countries[prices.index(max(prices))]}")
    st.write(f"Minimum: **{min(prices):.2f} USD/L** — {countries[prices.index(min(prices))]}")
    try:
        kz_price = prices[countries.index('Kazakhstan')]
        st.write(f"Kazakhstan: **{kz_price:.3f} USD/L**")
    except ValueError:
        st.write("Kazakhstan: Data not available")

if __name__ == "__main__":
    run_case1()