from app import db
from datetime import datetime

class Incident(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    service_id = db.Column(db.String(255), db.ForeignKey('service.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    urgency = db.Column(db.String(50))
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    service = db.relationship('Service', back_populates='incidents')

    def __repr__(self):
        return f'<Incident {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'status': self.status,
            'urgency': self.urgency,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
