📰 Times of India News Reader (AI-Powered)


[
]

A Streamlit web app that fetches the latest news from Times of India RSS feeds, generates AI-powered summaries, performs sentiment analysis, and provides text-to-speech audio for each news article.

✨ Features

🗂 Category Selection: Top Stories, India, Sports, Technology, Business, Entertainment, Science.

📰 Custom Number of Articles: Fetch 1–20 articles at a time.

🤖 AI Summaries: 4–5 line summaries using Google Gemini / GenAI.

😊😐😠 Sentiment Analysis: Understand the mood of each news article.

🎧 Text-to-Speech: Listen to news summaries in English.

🖼 Images: Displays featured images from news articles.

🎨 Modern UI: Gradient background and stylish buttons.

🛠 Tech Stack

Python 3.9+

Streamlit – Web app framework

Feedparser – Parse RSS feeds

BeautifulSoup – Extract and clean HTML content

Google Generative AI (Gemini) – AI summarization

TextBlob – Sentiment analysis

gTTS – Text-to-speech

Pillow (PIL) – Display images

Requests – HTTP requests

⚡ Installation

Clone the repository

git clone https://github.com/<your-username>/toi-news-reader.git
cd toi-news-reader


Create a virtual environment

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows


Install dependencies

pip install -r requirements.txt


Set up Google GenAI API key

Create a file .streamlit/secrets.toml:

GENAI_API_KEY = "your_google_gemini_api_key_here"

🚀 Run the App
streamlit run app.py


Open in browser: http://localhost:8501

📝 How to Use

🔹 Select a category from the sidebar.

🔹 Set the number of articles to fetch.

🔹 Click “Fetch News”.

🔹 Read AI-generated summaries, see sentiment, and listen via text-to-speech.

🔹 Click the link to read full news articles.

📂 Project Structure
toi-news-reader/
│
├─ app.py                 # Main Streamlit app
├─ requirements.txt       # Python dependencies
├─ README.md              # Project README
├─ .streamlit/
│   └─ secrets.toml       # API keys
├─ screenshots/           # Optional screenshots folder
└─ utils/
    └─ helper_functions.py  # Optional helper functions

💡 Future Improvements

🌐 Deploy to Streamlit Cloud for public access.

🗣 Multiple language support for text-to-speech.

📰 Add more news sources beyond Times of India.

⚡ Optimize performance with caching and better error handling.

🧑‍💻 Author

Developed by: Vanaja S
📄 License

MIT License © 2025 Vanaja S.
