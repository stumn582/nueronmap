from flask import Blueprint, render_template, request, jsonify
from decorators import login_required

game_bp = Blueprint("game", __name__, url_prefix="/game")

@game_bp.route("/", methods=["GET"])
@login_required
def game():
    return render_template("2048.html")

@game_bp.route("/score", methods=["POST"])
@login_required
def save_score():
    data = request.get_json(silent=True) or {}
    score = data.get("score", 0)
    return jsonify({"status": "ok", "score": score})

