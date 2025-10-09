from flask import Blueprint, request, jsonify
from backend.services import user_service

# prefix with /api
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    if not username or not name:
        return jsonify({"error": "Username and email are required"}), 400
    
    try:
        new_user = user_service.add_user(data)
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_service.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/', methods=['GET'])
def get_all_users():
    try:
        users = user_service.get_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        

    
