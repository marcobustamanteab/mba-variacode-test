import requests
from app import db
from app.models import Service, Incident, Team, EscalationPolicy, Schedule, User
from config import Config

class PagerDutyService:
    def __init__(self):
        self.base_url = Config.PAGERDUTY_BASE_URL
        self.headers = {
            'Authorization': f'Token token={Config.PAGERDUTY_API_KEY}',
            'Accept': 'application/vnd.pagerduty+json;version=2'
        }

    def _get(self, endpoint, params=None):
        response = requests.get(f'{self.base_url}/{endpoint}', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def sync_services(self):
        services_data = self._get('services')['services']
        for service_data in services_data:
            service = Service.query.get(service_data['id'])
            if not service:
                service = Service(id=service_data['id'])
            service.name = service_data['name']
            service.description = service_data.get('description')
            service.status = service_data['status']
            db.session.add(service)
        db.session.commit()

    def sync_incidents(self):
        incidents_data = self._get('incidents')['incidents']
        for incident_data in incidents_data:
            incident = Incident.query.get(incident_data['id'])
            if not incident:
                incident = Incident(id=incident_data['id'])
            incident.service_id = incident_data['service']['id']
            incident.status = incident_data['status']
            incident.urgency = incident_data['urgency']
            incident.title = incident_data['title']
            incident.description = incident_data['description']
            db.session.add(incident)
        db.session.commit()

    def sync_teams(self):
        teams_data = self._get('teams')['teams']
        for team_data in teams_data:
            team = Team.query.get(team_data['id'])
            if not team:
                team = Team(id=team_data['id'])
            team.name = team_data['name']
            team.description = team_data.get('description')
            db.session.add(team)
        db.session.commit()

    def sync_escalation_policies(self):
        policies_data = self._get('escalation_policies')['escalation_policies']
        for policy_data in policies_data:
            policy = EscalationPolicy.query.get(policy_data['id'])
            if not policy:
                policy = EscalationPolicy(id=policy_data['id'])
            policy.name = policy_data['name']
            policy.description = policy_data.get('description')
            policy.team_id = policy_data['team']['id'] if policy_data.get('team') else None
            db.session.add(policy)
        db.session.commit()

    def sync_schedules(self):
        schedules_data = self._get('schedules')['schedules']
        for schedule_data in schedules_data:
            schedule = Schedule.query.get(schedule_data['id'])
            if not schedule:
                schedule = Schedule(id=schedule_data['id'])
            schedule.name = schedule_data['name']
            schedule.time_zone = schedule_data['time_zone']
            schedule.description = schedule_data.get('description')
            db.session.add(schedule)
        db.session.commit()

    def sync_users(self):
        users_data = self._get('users')['users']
        for user_data in users_data:
            user = User.query.get(user_data['id'])
            if not user:
                user = User(id=user_data['id'])
            user.name = user_data['name']
            user.email = user_data['email']
            user.role = user_data['role']
            user.time_zone = user_data.get('time_zone')
            db.session.add(user)
        db.session.commit()
