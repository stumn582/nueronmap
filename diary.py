from flask import Blueprint, render_template, request, redirect, session
from decorators import login_required
import boto3
import sqlite3

diary_bp = Blueprint("diary", __name__)

# AWS Comprehend
comprehend = boto3.client(
    "comprehend",
    region_name="ap-northeast-2"
)

@diary_bp.route("/diary", methods=["GET"])
@login_required
def diary():
    return render_template("diary.html", diary="", result=None)

@diary_bp.route("/diary/analyze", methods=["POST"])
@login_required
def analyze_diary():
    diary_text = request.form.get("diary", "").strip()
    if not diary_text:
        return redirect("/diary")

    # ✅ 영어로 분석 (정확도 확보)
    response = comprehend.detect_sentiment(
        Text=diary_text,
        LanguageCode="en"
    )

    score = response["SentimentScore"]

    # ✅ Mixed 제외하고 dominant 계산
    filtered_score = {
        "POSITIVE": score["Positive"],
        "NEGATIVE": score["Negative"],
        "NEUTRAL": score["Neutral"],
    }

    dominant = max(filtered_score, key=filtered_score.get)

    # DB 저장
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO emotion_logs (user_id, diary, emotion, dominant)
        VALUES (?, ?, ?, ?)
    """, (
        session["user_id"],
        diary_text,
        dominant,
        dominant
    ))
    conn.commit()
    conn.close()

    return render_template(
        "diary.html",
        diary=diary_text,
        result={
            "emotion": dominant,
            "dominant": dominant,
            "score": filtered_score
        }
    )

