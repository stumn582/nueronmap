from flask import Blueprint, render_template
from decorators import login_required
import sqlite3

stats_bp = Blueprint("stats", __name__)

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@stats_bp.route("/stats")
@login_required
def stats():
    conn = get_db()
    cur = conn.cursor()

    # 1. 감정 비율 (대문자로 통일해서 집계)
    cur.execute("""
        SELECT UPPER(dominant) as dominant, COUNT(*) as count
        FROM emotion_logs
        GROUP BY UPPER(dominant)
    """)
    emotion_stats = cur.fetchall()

    # 2. 2048 최고 점수
    cur.execute("""
        SELECT MAX(score) as max_score
        FROM game_scores
    """)
    max_score = cur.fetchone()["max_score"]

    # 3. 최근 점수 5개
    cur.execute("""
        SELECT score, created_at
        FROM game_scores
        ORDER BY created_at DESC
        LIMIT 5
    """)
    recent_scores = cur.fetchall()

    # ================================
    # 4. 달력용 감정 데이터 (날짜별)
    # ================================
    cur.execute("""
        SELECT DATE(created_at) as date, UPPER(dominant) as emotion
        FROM emotion_logs
    """)
    rows = cur.fetchall()

    emotion_map = {}
    for row in rows:
        emotion_map[row["date"]] = row["emotion"].lower()

    # ================================
    # 5. 감정 변화 그래프 데이터
    # ================================
    cur.execute("""
        SELECT strftime('%m-%d', created_at) as date, UPPER(dominant) as emotion
        FROM emotion_logs
        ORDER BY created_at DESC
        LIMIT 7
    """)
    emotion_rows = cur.fetchall()

    emotion_dates = []
    emotion_scores = []

    for row in reversed(emotion_rows):
        emotion_dates.append(row["date"])

        if row["emotion"] == "POSITIVE":
            emotion_scores.append(1)
        elif row["emotion"] == "NEUTRAL":
            emotion_scores.append(0)
        else:
            emotion_scores.append(-1)

    # ================================
    # 6. 오늘의 한마디
    # ================================
    today_quote = "지금 이 순간도 충분히 잘하고 있어요 🙂"

    # ================================
    # 7. 감정 & 게임 상관관계
    # ================================
    relation = {
        "positive": 0,
        "neutral": 0,
        "negative": 0
    }

    cur.execute("""
        SELECT UPPER(e.dominant) as emotion, AVG(g.score) as avg_score
        FROM emotion_logs e
        JOIN game_scores g ON DATE(e.created_at) = DATE(g.created_at)
        GROUP BY UPPER(e.dominant)
    """)
    relation_rows = cur.fetchall()

    for row in relation_rows:
        if row["emotion"] == "POSITIVE":
            relation["positive"] = int(row["avg_score"])
        elif row["emotion"] == "NEUTRAL":
            relation["neutral"] = int(row["avg_score"])
        elif row["emotion"] == "NEGATIVE":
            relation["negative"] = int(row["avg_score"])


    conn.close()

    return render_template(
        "stats.html",
        emotion_stats=emotion_stats,
        max_score=max_score,
        recent_scores=recent_scores,
        emotion_map=emotion_map,
        emotion_dates=emotion_dates,
        emotion_scores=emotion_scores,
        today_quote=today_quote,
        relation=relation
    )



