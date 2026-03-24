import json, os
from flask import Blueprint, jsonify, abort

alumni_bp = Blueprint("alumni", __name__)
DATA = json.load(open(os.path.join(os.path.dirname(__file__), "../data/alumni.json")))

@alumni_bp.get("/api/alumni")
def list_alumni():
    industry = __import__("flask").request.args.get("industry")
    availability = __import__("flask").request.args.get("availability")
    result = DATA
    if industry:
        result = [a for a in result if a["industry"].lower() == industry.lower()]
    if availability:
        result = [a for a in result if a["availability"] == availability]
    return jsonify(result)

@alumni_bp.get("/api/alumni/<string:alumni_id>")
def get_alumni(alumni_id):
    match = next((a for a in DATA if a["id"] == alumni_id), None)
    if not match:
        abort(404)
    return jsonify(match)
