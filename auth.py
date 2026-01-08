from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth = Blueprint("auth", __name__)

# ========================
# 로그인
# ========================
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # 🔑 관리자 계정 (하드코딩)
        if username == "stumna" and password == "whdwhdwhd1%":
            session.clear()
            session["user_id"] = "admin"
            session["username"] = "stumna"
            session["is_admin"] = True
            return redirect("/")

        # 👤 일반 사용자
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT id, password, role FROM users WHERE username = ?",
            (username,)
        )
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session.clear()
            session["user_id"] = user[0]
            session["username"] = username
            session["is_admin"] = (user[2] == "admin")
            return redirect("/")

        return render_template("login.html", error="아이디 또는 비밀번호가 틀렸습니다.")

    return render_template("login.html")


# ========================
# 회원가입
# ========================
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_pw, "user")
            )
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="이미 존재하는 사용자입니다.")

        return redirect("/login")

    return render_template("register.html")


# ========================
# 로그아웃
# ========================
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

