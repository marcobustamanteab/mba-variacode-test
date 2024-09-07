from app import db
from datetime import datetime

class Team(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    services = db.relationship('Service', secondary='service_team', back_populates='teams')
    escalation_policies = db.relationship('EscalationPolicy', back_populates='team')

    def __repr__(self):
        return f'<Team {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

service_team = db.Table('service_team',
    db.Column('service_id', db.String(255), db.ForeignKey('service.id'), primary_key=True),
    db.Column('team_id', db.String(255), db.ForeignKey('team.id'), primary_key=True)
)
