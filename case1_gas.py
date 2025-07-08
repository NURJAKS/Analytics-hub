import matplotlib.pyplot as plt
import streamlit as st

def run_case1():
    st.header("⛽ Цены на бензин по странам (Case 1)")

    # 🔁 Реальные данные (июль 2025)
    countries = [
        "Norway", "Netherlands", "Germany", "Finland", "Italy",
        "USA", "Malaysia", "Venezuela", "Iran", "Kazakhstan"
    ]
    prices = [
        2.09, 2.01, 1.96, 1.92, 1.92,
        1.30, 0.49, 0.50, 0.029, 0.47
    ]

    st.subheader("📊 Данные (USD за литр)")
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(countries, prices, color='skyblue')

    for i, country in enumerate(countries):
        if country == "Kazakhstan":
            bars[i].set_color("orange")
            ax.text(i, prices[i] + 0.05, "🇰🇿", ha='center')

    ax.set_title("Цены на бензин по странам", fontsize=16)
    ax.set_ylabel("Цена (USD)")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig)

    st.subheader("📈 Аналитика")
    st.write(f"🔺 Максимум: **{max(prices):.2f} USD** — {countries[prices.index(max(prices))]}")
    st.write(f"🔻 Минимум: **{min(prices):.2f} USD** — {countries[prices.index(min(prices))]}")
    st.write(f"📍 Казахстан: **{prices[countries.index('Kazakhstan')]:.3f} USD**")
