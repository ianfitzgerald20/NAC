import json, os
from flask import Blueprint, jsonify, request, abort

jobs_bp = Blueprint("jobs", __name__)
DATA = json.load(open(os.path.join(os.path.dirname(__file__), "../data/jobs.json")))

@jobs_bp.get("/api/jobs")
def list_jobs():
    industry = request.args.get("industry")
    job_type = request.args.get("type")
    result = DATA
    if industry:
        result = [j for j in result if j["industry"].lower() == industry.lower()]
    if job_type:
        result = [j for j in result if j["type"] == job_type]
    return jsonify(result)

@jobs_bp.get("/api/jobs/<int:job_id>")
def get_job(job_id):
    match = next((j for j in DATA if j["id"] == job_id), None)
    if not match:
        abort(404)
    return jsonify(match)
