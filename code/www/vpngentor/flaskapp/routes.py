# website/routes.py

from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return jsonify({"message": "Welcome to VPNBot Website!"})

def register_routes(app):
    app.register_blueprint(main_bp)
