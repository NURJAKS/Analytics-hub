import feedparser
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

def get_news_titles(rss_url):
    feed = feedparser.parse(rss_url)
    return [entry.title for entry in feed.entries]

def analyze_words(titles):
    text = ' '.join(titles).lower()
    words = re.findall(r'\b\w{4,}\b', text)

    stop_words = {
        'this', 'that', 'with', 'from', 'have', 'been', 'will',
        'your', 'about', 'their', 'what', 'when', 'which',
        'these', 'those', 'after', 'before', 'more', 'such',
        'very', 'some', 'over', 'than', 'then', 'into', 'they',
        'them', 'would', 'could', 'also', 'just', 'like', 'want',
        'https', 'feed', 'href', 'html', 'link', 'title', 'news',
        'and', 'for', 'are', 'the', 'you', 'was', 'were', 'has',
        'had', 'not', 'but', 'out', 'now'
    }

    filtered = [word for word in words if word not in stop_words]
    return Counter(filtered)

def run_case3():
    st.header("📰 Анализ заголовков новостей (Case 3)")

    rss_urls = [
        "https://habr.com/ru/rss/all/",
        "https://techxplore.com/feeds/all.xml",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://www.wired.com/feed/rss",
        "https://feeds.feedburner.com/TheHackersNews"
    ]

    all_titles = []
    for url in rss_urls:
        titles = get_news_titles(url)
        all_titles.extend(titles)

    st.success(f"🔎 Всего заголовков получено: {len(all_titles)}")
    st.markdown("🔹 **Примеры заголовков:**")
    for title in all_titles[:5]:
        st.write("-", title)

    word_counts = analyze_words(all_titles)

    # Топ-10 слов
    top_words = word_counts.most_common(10)
    words, counts = zip(*top_words)

    st.subheader("📊 Топ-10 самых частых слов")
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(words, counts, color='skyblue')
    ax.set_title("Частота слов")
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)

    # Облако слов
    st.subheader("☁ Облако слов")
    wc = WordCloud(width=1000, height=500, background_color='white', colormap='viridis')
    wc.generate_from_frequencies(word_counts)
    fig_wc, ax_wc = plt.subplots(figsize=(14, 7))
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)
