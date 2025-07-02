from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeSerializer

auth_bp = Blueprint('auth', __name__)
serializer = URLSafeSerializer("another-secret-key")

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user = User(email=data['email'], password=data['password'], role='client')
    db.session.add(user)
    db.session.commit()
    token = serializer.dumps({'user_id': user.id})
    return jsonify({'verification_url': f'/verify/{token}'})

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        data = serializer.loads(token)
        user = User.query.get(data['user_id'])
        user.is_verified = True
        db.session.commit()
        return jsonify({'message': 'Email verified'})
    except:
        return jsonify({'error': 'Invalid token'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'access_token': token})