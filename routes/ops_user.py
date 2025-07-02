from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, File
import os

ops_bp = Blueprint('ops', __name__)

@ops_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    user = get_jwt_identity()
    if user['role'] != 'ops':
        return jsonify({'error': 'Only ops users can upload'}), 403
    file = request.files['file']
    if file.filename.split('.')[-1] not in ['pptx', 'docx', 'xlsx']:
        return jsonify({'error': 'Invalid file type'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    db.session.add(File(filename=filename, uploader_id=user['id']))
    db.session.commit()
    return jsonify({'message': 'File uploaded'})