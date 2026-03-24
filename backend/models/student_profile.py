import json
from database import db


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    grad_year = db.Column(db.Integer)
    grade = db.Column(db.String(20))
    interests = db.Column(db.Text)  # JSON array stored as string

    def to_dict(self):
        return {
            "gradYear": self.grad_year,
            "grade": self.grade,
            "interests": json.loads(self.interests) if self.interests else [],
        }
