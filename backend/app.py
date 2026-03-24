from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from database import db
import models  # registers all models with SQLAlchemy
from routes.alumni import alumni_bp
from routes.jobs import jobs_bp
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(__file__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'bulldogconnect.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-in-production")

db.init_app(app)
JWTManager(app)

app.register_blueprint(alumni_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(auth_bp)

FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
PAGES_DIR = os.path.join(FRONTEND_DIR, "pages")

@app.get("/")
def root():
    return send_from_directory(PAGES_DIR, "index.html")

@app.get("/app")
def app_page():
    return send_from_directory(PAGES_DIR, "app.html")

@app.get("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    app.run(debug=True, port=port)
