from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

# Aquí puedes agregar más rutas según sea necesario
