from flask import Flask, render_template
from news import news_bp
from auth import auth as auth_bp
from admin import admin_bp
from diary import diary_bp
from game import game_bp
from stats import stats_bp
from recommend import recommend_bp

app = Flask(__name__)
app.secret_key = "secret"

app.register_blueprint(news_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(diary_bp)
app.register_blueprint(game_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(recommend_bp)


@app.route("/")
def index():
    return render_template("index.html")

