from flask import Blueprint, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import URLSafeSerializer
from models import db, File, DownloadLink

client_bp = Blueprint('client', __name__)
serializer = URLSafeSerializer("another-secret-key")

@client_bp.route('/files', methods=['GET'])
@jwt_required()
def list_files():
    user = get_jwt_identity()
    if user['role'] != 'client':
        return jsonify({'error': 'Access denied'}), 403
    files = File.query.all()
    return jsonify([{'id': f.id, 'name': f.filename} for f in files])

@client_bp.route('/download/<int:file_id>', methods=['GET'])
@jwt_required()
def generate_link(file_id):
    user = get_jwt_identity()
    if user['role'] != 'client':
        return jsonify({'error': 'Access denied'}), 403
    token = serializer.dumps({'file_id': file_id, 'client_id': user['id']})
    db.session.add(DownloadLink(file_id=file_id, client_id=user['id'], token=token))
    db.session.commit()
    return jsonify({'download_link': f'/download-file/{token}'})

@client_bp.route('/download-file/<token>', methods=['GET'])
@jwt_required()
def download_file(token):
    user = get_jwt_identity()
    try:
        data = serializer.loads(token)
        if data['client_id'] != user['id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        file = File.query.get(data['file_id'])
        return send_from_directory('uploads', file.filename, as_attachment=True)
    except:
        return jsonify({'error': 'Invalid token'}), 400