from flask import Flask
from models import db
from routes.api import api_bp
from routes.views import views_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Ruta absoluta de la base de datos SQLite
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'db', 'creditos.db')
    
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Crear el directorio de la base de datos si no existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Inicialización de la base de datos con la aplicación
    db.init_app(app)
    
    # Registro de blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(views_bp)
    
    # Inicialización de la base de datos
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)