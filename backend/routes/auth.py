from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models.user import User
from models.alumni_profile import AlumniProfile
from models.student_profile import StudentProfile

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/register")
def register():
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()
    password = body.get("password", "")
    role = body.get("role", "student")
    first_name = body.get("firstName", "").strip()
    last_name = body.get("lastName", "").strip()

    if not all([email, password, first_name, last_name]):
        return jsonify({"error": "All fields are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if role not in ("student", "alumni"):
        return jsonify({"error": "Invalid role"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        first_name=first_name,
        last_name=last_name,
    )
    db.session.add(user)
    db.session.flush()

    if role == "alumni":
        db.session.add(AlumniProfile(
            user_id=user.id,
            company=body.get("company", ""),
            job_title=body.get("jobTitle", ""),
            grad_year=body.get("gradYear"),
            college=body.get("college", ""),
            industry=body.get("industry", ""),
            availability="available",
        ))
    else:
        db.session.add(StudentProfile(
            user_id=user.id,
            grad_year=body.get("gradYear"),
            grade=body.get("grade", ""),
        ))

    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "role": role, "user": user.to_dict()}), 201


@auth_bp.post("/api/auth/login")
def login():
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()
    password = body.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "role": user.role, "user": user.to_dict()})


@auth_bp.get("/api/auth/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = user.to_dict()

    if user.role == "student" and user.student_profile:
        data["profile"] = user.student_profile.to_dict()
    elif user.role == "alumni" and user.alumni_profile:
        data["profile"] = user.alumni_profile.to_dict()
    else:
        data["profile"] = {}

    return jsonify(data)


@auth_bp.put("/api/auth/me")
@jwt_required()
def update_me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found"}), 404

    body = request.get_json(silent=True) or {}

    # Update name fields on User
    if body.get("firstName"):
        user.first_name = body["firstName"].strip()
    if body.get("lastName"):
        user.last_name = body["lastName"].strip()

    if user.role == "alumni":
        p = user.alumni_profile
        if not p:
            p = AlumniProfile(user_id=user.id)
            db.session.add(p)
        p.job_title   = body.get("jobTitle",   p.job_title   or "")
        p.company     = body.get("company",    p.company     or "")
        p.college     = body.get("college",    p.college     or "")
        p.industry    = body.get("industry",   p.industry    or "")
        p.grad_year   = body.get("gradYear",   p.grad_year)
        p.bio         = body.get("bio",        p.bio         or "")
        p.linkedin_url = body.get("linkedinUrl", p.linkedin_url or "")
        p.availability = body.get("availability", p.availability or "available")

    elif user.role == "student":
        p = user.student_profile
        if not p:
            p = StudentProfile(user_id=user.id)
            db.session.add(p)
        p.grad_year = body.get("gradYear", p.grad_year)
        p.grade     = body.get("grade",    p.grade or "")

    db.session.commit()
    return jsonify({"message": "Profile saved"})
