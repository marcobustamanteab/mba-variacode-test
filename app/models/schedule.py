from app import db
from datetime import datetime

class Schedule(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    time_zone = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship('User', secondary='schedule_user', back_populates='schedules')

    def __repr__(self):
        return f'<Schedule {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'time_zone': self.time_zone,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

schedule_user = db.Table('schedule_user',
    db.Column('schedule_id', db.String(255), db.ForeignKey('schedule.id'), primary_key=True),
    db.Column('user_id', db.String(255), db.ForeignKey('user.id'), primary_key=True)
)
