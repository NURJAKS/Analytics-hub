import streamlit as st
from case1_gas import run_case1
from case2_weather import run_case2
from case3_rss import run_case3  # твой готовый кейс

st.set_page_config(
    page_title="Аналитика 3-ТУР",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Финальный Проект — 3-ТУР: Аналитика и Дата Сайнс")
st.markdown("Выберите кейс для анализа:")

tab1, tab2, tab3 = st.tabs(["⛽ Бензин", "🌤 Погода", "📰 RSS-заголовки"])

with tab1:
    run_case1()

with tab2:
    run_case2()

with tab3:
    run_case3()
