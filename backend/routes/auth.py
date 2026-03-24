from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

# Stub auth — replace with real DB + hashed passwords
USERS = {}

@auth_bp.post("/api/auth/register")
def register():
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()
    role = body.get("role", "student")
    if not email:
        return jsonify({"error": "email required"}), 400
    if email in USERS:
        return jsonify({"error": "already registered"}), 409
    USERS[email] = {"email": email, "role": role, "profile": body}
    return jsonify({"token": f"stub-token-{email}", "role": role}), 201

@auth_bp.post("/api/auth/login")
def login():
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()
    role = body.get("role", "student")
    if not email:
        return jsonify({"error": "email required"}), 400
    # Stub: accept any credentials
    return jsonify({"token": f"stub-token-{email}", "role": role})
