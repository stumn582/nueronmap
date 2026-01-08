from flask import Blueprint, render_template, session
import sqlite3
import requests
import os

recommend_bp = Blueprint("recommend", __name__, url_prefix="/recommend")

NEWS_API_KEY = os.getenv("NEWSAPI_KEY")

# 감정 → 키워드 매핑
EMOTION_KEYWORD_MAP = {
    "HAPPY": ["success", "festival", "celebration", "entertainment"],
    "SAD": ["healing", "hope", "inspiration", "good news"],
    "ANGRY": ["justice", "crime", "law", "investigation"],
    "CALM": ["nature", "travel", "meditation", "peace"],
    "CONFUSED": ["analysis", "explainer", "insight"],
    "FEAR": ["safety", "recovery", "support"]
}

@recommend_bp.route("/")
def recommend():
    if "user_id" not in session:
        return render_template("recommend.html", articles=[], emotion=None)

    user_id = session["user_id"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 👉 emotion_logs 테이블에서 가장 최근 감정(dominant) 가져오기
    cursor.execute(
        "SELECT dominant FROM emotion_logs WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return render_template("recommend.html", articles=[], emotion=None)

    emotion = row[0]

    keywords = EMOTION_KEYWORD_MAP.get(emotion, ["news"])
    query = " OR ".join(keywords)

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        print("DEBUG STATUS:", response.status_code)
        print("DEBUG TEXT:", response.text)
        data = response.json()
        articles = data.get("articles", [])
    except Exception as e:
        print("Recommend API Error:", e)
        articles = []

    return render_template("recommend.html", articles=articles, emotion=emotion)

