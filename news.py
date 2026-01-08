# news.py
import os
import requests
from flask import Blueprint, render_template, request, flash

news_bp = Blueprint("news", __name__)

NEWS_API_KEY = os.environ.get("NEWSAPI_KEY")

@news_bp.route("/news", methods=["GET", "POST"])
def news():
    articles = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if not query:
            flash("검색어를 입력하세요.")
            return render_template("news.html", articles=articles, query=query)

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "ko",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": NEWS_API_KEY
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
        except Exception as e:
            print("NewsAPI ERROR:", e)
            flash("뉴스 검색 중 오류가 발생했습니다.")

    return render_template("news.html", articles=articles, query=query)

