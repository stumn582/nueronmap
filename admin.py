from flask import Blueprint, render_template, session
from decorators import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@admin_required
def admin_home():
    return render_template("admin.html")

