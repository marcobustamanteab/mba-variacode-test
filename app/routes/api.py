from flask import Blueprint, jsonify, request
from app.services.pagerduty_service import PagerDutyService
from app.models import Service, Incident, Team, EscalationPolicy, User, Schedule
from app import db
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from itertools import groupby

bp = Blueprint('api', __name__)
pd_service = PagerDutyService()

@bp.route('/sync_data', methods=['POST'])
def sync_data():
    try:
        pd_service.sync_services()
        pd_service.sync_incidents()
        pd_service.sync_teams()
        pd_service.sync_escalation_policies()
        pd_service.sync_schedules()
        pd_service.sync_users()
        return jsonify({"message": "Data synced successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services]), 200

@bp.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([i.to_dict() for i in incidents]), 200

@bp.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([t.to_dict() for t in teams]), 200

@bp.route('/escalation_policies', methods=['GET'])
def get_escalation_policies():
    policies = EscalationPolicy.query.all()
    return jsonify([p.to_dict() for p in policies]), 200

@bp.route('/analytics', methods=['GET'])
def get_analytics():
    services_count = Service.query.count()
    incidents_per_service = db.session.query(Service.name, db.func.count(Incident.id)).join(Incident).group_by(Service.id).all()
    incidents_by_status = db.session.query(Service.name, Incident.status, db.func.count(Incident.id)).join(Incident).group_by(Service.id, Incident.status).all()
    teams_count = Team.query.count()
    services_per_team = db.session.query(Team.name, db.func.count(Service.id)).join(Team.services).group_by(Team.id).all()
    escalation_policies_count = EscalationPolicy.query.count()
    
    analytics = {
        "services_count": services_count,
        "incidents_per_service": dict(incidents_per_service),
        "incidents_by_status": {s: {status: count for _, status, count in incidents} for s, incidents in groupby(incidents_by_status, key=lambda x: x[0])},
        "teams_count": teams_count,
        "services_per_team": dict(services_per_team),
        "escalation_policies_count": escalation_policies_count
    }
    
    return jsonify(analytics), 200

@bp.route('/reports/csv', methods=['GET'])
def get_csv_reports():
    df_services = pd.DataFrame([(s.id, s.name) for s in Service.query.all()], columns=['id', 'name'])
    df_incidents = pd.DataFrame([(i.id, i.service_id, i.status) for i in Incident.query.all()], columns=['id', 'service_id', 'status'])
    df_teams = pd.DataFrame([(t.id, t.name) for t in Team.query.all()], columns=['id', 'name'])
    df_policies = pd.DataFrame([(p.id, p.name, p.team_id) for p in EscalationPolicy.query.all()], columns=['id', 'name', 'team_id'])

    csv_files = {
        'services.csv': df_services.to_csv(index=False),
        'incidents.csv': df_incidents.to_csv(index=False),
        'teams.csv': df_teams.to_csv(index=False),
        'escalation_policies.csv': df_policies.to_csv(index=False)
    }

    return jsonify(csv_files), 200

@bp.route('/analytics/incidents', methods=['GET'])
def get_incidents_analysis():
    incidents_per_service = db.session.query(Service.name, db.func.count(Incident.id)).join(Incident).group_by(Service.id).all()
    service_with_most_incidents = max(incidents_per_service, key=lambda x: x[1])
    
    incidents_by_status = db.session.query(Service.name, Incident.status, db.func.count(Incident.id))\
        .join(Incident)\
        .filter(Service.name == service_with_most_incidents[0])\
        .group_by(Service.id, Incident.status).all()
    
    analysis = {
        "service_with_most_incidents": {
            "name": service_with_most_incidents[0],
            "incident_count": service_with_most_incidents[1],
            "incidents_by_status": {status: count for _, status, count in incidents_by_status}
        }
    }
    
    return jsonify(analysis), 200

@bp.route('/analytics/incidents/graph', methods=['GET'])
def get_incidents_graph():
    incidents_per_service = db.session.query(Service.name, db.func.count(Incident.id)).join(Incident).group_by(Service.id).all()
    
    services = [i[0] for i in incidents_per_service]
    incident_counts = [i[1] for i in incidents_per_service]
    
    plt.figure(figsize=(10, 5))
    plt.bar(services, incident_counts)
    plt.title('Incidents per Service')
    plt.xlabel('Services')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=45, ha='right')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return jsonify({"graph": graphic}), 200

@bp.route('/analytics/inactive_users', methods=['GET'])
def get_inactive_users():
    active_users = db.session.query(User.id).join(Schedule.users).distinct().subquery()
    inactive_users = User.query.filter(~User.id.in_(active_users)).all()
    
    return jsonify([u.to_dict() for u in inactive_users]), 200
