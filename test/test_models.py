import pytest
from app.models import Service, Incident, Team, EscalationPolicy

def test_service_model():
    service = Service(id="1", name="Test Service")
    assert service.id == "1"
    assert service.name == "Test Service"

def test_incident_model():
    incident = Incident(id="1", service_id="1", status="triggered")
    assert incident.id == "1"
    assert incident.service_id == "1"
    assert incident.status == "triggered"

def test_team_model():
    team = Team(id="1", name="Test Team")
    assert team.id == "1"
    assert team.name == "Test Team"

def test_escalation_policy_model():
    policy = EscalationPolicy(id="1", name="Test Policy", team_id="1")
    assert policy.id == "1"
    assert policy.name == "Test Policy"
    assert policy.team_id == "1"