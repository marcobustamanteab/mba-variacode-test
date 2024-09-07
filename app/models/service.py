from app import db
from datetime import datetime

class Service(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    incidents = db.relationship('Incident', back_populates='service')
    teams = db.relationship('Team', secondary='service_team', back_populates='services')
    escalation_policies = db.relationship('EscalationPolicy', secondary='service_escalation_policy', back_populates='services')

    def __repr__(self):
        return f'<Service {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
