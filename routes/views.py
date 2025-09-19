from flask import Blueprint, render_template

# Definición del blueprint para las vistas
views_bp = Blueprint('views', __name__)

# Ruta para la vista de inicio
@views_bp.route('/')
def home():
    return render_template('creditos.html', title='Inicio')