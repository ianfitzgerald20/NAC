from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from routes.alumni import alumni_bp
from routes.jobs import jobs_bp
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(alumni_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(auth_bp)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")

@app.get("/")
def root():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    app.run(debug=True, port=port)
