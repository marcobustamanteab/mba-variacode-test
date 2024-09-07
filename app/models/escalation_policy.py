from app import db
from datetime import datetime

class EscalationPolicy(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    team_id = db.Column(db.String(255), db.ForeignKey('team.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = db.relationship('Team', back_populates='escalation_policies')
    services = db.relationship('Service', secondary='service_escalation_policy', back_populates='escalation_policies')

    def __repr__(self):
        return f'<EscalationPolicy {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'team_id': self.team_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

service_escalation_policy = db.Table('service_escalation_policy',
    db.Column('service_id', db.String(255), db.ForeignKey('service.id'), primary_key=True),
    db.Column('escalation_policy_id', db.String(255), db.ForeignKey('escalation_policy.id'), primary_key=True)
)
