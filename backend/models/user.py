from database import db
from datetime import datetime, timezone


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'alumni'
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_verified = db.Column(db.Boolean, default=False)

    alumni_profile = db.relationship("AlumniProfile", backref="user", uselist=False)
    student_profile = db.relationship("StudentProfile", backref="user", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "createdAt": self.created_at.isoformat(),
        }
