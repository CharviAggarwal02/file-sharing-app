from flask import Flask
from models import db
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.ops_user import ops_bp
from routes.client_user import client_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'another-secret-key'

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(ops_bp)
app.register_blueprint(client_bp)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)