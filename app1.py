import streamlit as st
import requests
import feedparser
import urllib3
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import google.generativeai as genai  # Gemini / Google GenAI
from gtts import gTTS
import base64
from textblob import TextBlob

# -------------------- CONFIG --------------------
# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Times of India RSS feeds by category
TOI_FEEDS = {
    "Top Stories": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "India": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "Sports": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    "Technology": "https://timesofindia.indiatimes.com/rssfeeds/66949506.cms",
    "Business": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
    "Entertainment": "https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms",
    "Science": "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms"
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Configure GenAI
genai.configure(api_key=st.secrets["GENAI_API_KEY"])  # Replace with your Gemini API key

# -------------------- STREAMLIT LAYOUT --------------------
st.set_page_config(page_title="📰 Times of India News Reader", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e, #16213e, #0f3460);
            color: white;
            padding: 20px;
        }
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #00f5d4 !important;
            font-weight: bold;
            text-shadow: 0px 0px 6px rgba(0, 245, 212, 0.7);
        }
        .stButton>button {
            background: linear-gradient(90deg, #00f5d4, #00bbf9);
            color: black;
            font-weight: bold;
            border-radius: 12px;
            padding: 8px 16px;
            border: none;
            box-shadow: 0px 0px 10px rgba(0,245,212,0.6);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #00bbf9, #00f5d4);
            transform: scale(1.05);
            box-shadow: 0px 0px 20px rgba(0,245,212,0.9);
        }
    </style>
""", unsafe_allow_html=True)

# ---------- App Title ----------
st.title("📰 Times of India News Reader")
st.subheader("🤖 Get the latest news with AI-powered summaries")

# ---------- Sidebar ----------
st.sidebar.header("⚙️ AI Settings")
selected_category = st.sidebar.selectbox("📌 Select Category", list(TOI_FEEDS.keys()))
max_articles = st.sidebar.slider("📰 Number of Articles", min_value=1, max_value=20, value=5)
fetch_button = st.sidebar.button("🚀 Fetch News")

# -------------------- FUNCTIONS --------------------
def extract_image(entry):
    if "media_content" in entry and len(entry.media_content) > 0:
        return entry.media_content[0].get("url")
    elif "enclosures" in entry and len(entry.enclosures) > 0:
        return entry.enclosures[0].get("url")
    elif "summary" in entry:
        soup = BeautifulSoup(entry.summary, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
    return None

def fetch_rss_news(feed_url, max_articles=10):
    articles = []
    try:
        response = requests.get(feed_url, headers=HEADERS, verify=False)
        feed = feedparser.parse(response.content)
        for entry in feed.entries[:max_articles]:
            article = {
                "title": entry.get("title"),
                "description": BeautifulSoup(entry.get("summary", entry.get("description", "")), "html.parser").get_text(),
                "url": entry.get("link"),
                "published": entry.get("published", entry.get("pubDate", "N/A")),
                "image_url": extract_image(entry)
            }
            articles.append(article)
    except Exception as e:
        st.error(f"❌ Error fetching feed: {e}")
    return articles

def summarize_news_with_genai(text):
    """Summarize news in 4-5 lines using GenAI."""
    try:
        response = genai.chat.completions.create(
            model="chat-bison-001",
            messages=[{"role": "user", "content": f"Summarize the following news in 4-5 lines:\n{text}"}],
            temperature=0.5,
        )
        summary = response.candidates[0].content
        return summary
    except:
        return text[:300] + "..."  # fallback if GenAI fails

# 🎧 Text-to-Speech
def text_to_speech(summary_text, lang="en"):
    try:
        tts = gTTS(text=summary_text, lang=lang)
        tts.save("summary.mp3")
        with open("summary.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        audio_html = f"""
            <audio controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        return audio_html
    except Exception as e:
        return f"⚠️ Voice failed: {e}"

# 😊 Sentiment Analysis with Emojis
def get_sentiment_emoji(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "😊 Positive"
    elif polarity < -0.2:
        return "😠 Negative"
    else:
        return "😐 Neutral"

# -------------------- DISPLAY --------------------
if fetch_button:
    feed_url = TOI_FEEDS[selected_category]
    articles = fetch_rss_news(feed_url, max_articles=max_articles)

    if not articles:
        st.warning("⚠️ No articles found for this category.")
    else:
        # 🎯 Trending News
        with st.container():
            st.markdown(
                """
                <div style="
                    background-color:#fff3e6;
                    padding:20px;
                    border-radius:15px;
                    box-shadow:0 4px 10px rgba(0,0,0,0.1);
                    margin-bottom:20px;">
                    <h2 style="color:#d35400;">🔥 Trending News</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            top_article = articles[0]
            st.subheader(top_article["title"])
            st.write(f"🗓️ **Published:** {top_article['published']}")

            summary = summarize_news_with_genai(top_article["description"])
            st.markdown(
                f"""
                <div style="
                    background:linear-gradient(135deg, #f0f8ff, #e8f6ff);
                    padding:15px;
                    border-radius:12px;
                    font-style:italic;
                    color:#2c3e50;
                    margin-top:10px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1);">
                    ✨ <b>AI Summary:</b><br>{summary}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Sentiment
            sentiment = get_sentiment_emoji(summary)
            st.write(f"**Sentiment:** {sentiment}")

            # Voice
            audio_html = text_to_speech(summary)
            st.markdown(audio_html, unsafe_allow_html=True)

            if top_article["image_url"]:
                try:
                    response = requests.get(top_article["image_url"], verify=False)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True, caption="Trending Highlight")
                except:
                    st.info("🖼️ Image could not be loaded.")

        st.markdown("---")

        # Other News
        st.markdown("## 📰📌 Other News")
        for idx, article in enumerate(articles[1:], start=2):
            st.markdown(f"<div class='news-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='news-title'>{idx}. {article['title']}</div>", unsafe_allow_html=True)
            st.write(f"🗓️ **Published:** {article['published']}")

            summary = summarize_news_with_genai(article["description"])

            with st.expander("🔎 AI Summary", expanded=True):
                st.markdown(
                    f"""
                    <div style="
                        background-color:#f9f9f9;
                        padding:12px;
                        border-left:4px solid #3498db;
                        border-radius:8px;
                        font-style:italic;
                        color:#34495e;">
                        {summary}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Sentiment + Voice
                sentiment = get_sentiment_emoji(summary)
                st.write(f"**Sentiment:** {sentiment}")
                audio_html = text_to_speech(summary)
                st.markdown(audio_html, unsafe_allow_html=True)

            st.markdown(f"[👉 Read full article]({article['url']})", unsafe_allow_html=True)
            if article['image_url']:
                try:
                    response = requests.get(article['image_url'], verify=False)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True)
                except:
                    st.info("Image could not be loaded.")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
