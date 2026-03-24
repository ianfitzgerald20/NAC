import json
from database import db


class AlumniProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company = db.Column(db.String(120))
    job_title = db.Column(db.String(120))
    grad_year = db.Column(db.Integer)
    college = db.Column(db.String(120))
    degree = db.Column(db.String(120))
    industry = db.Column(db.String(80))
    tags = db.Column(db.Text)  # JSON array stored as string
    availability = db.Column(db.String(20), default="available")
    linkedin_url = db.Column(db.String(256))
    bio = db.Column(db.Text)

    def to_dict(self):
        return {
            "company": self.company,
            "jobTitle": self.job_title,
            "gradYear": self.grad_year,
            "college": self.college,
            "degree": self.degree,
            "industry": self.industry,
            "tags": json.loads(self.tags) if self.tags else [],
            "availability": self.availability,
            "linkedinUrl": self.linkedin_url,
            "bio": self.bio,
        }
