# Definición de rutas API para la gestión de créditos
# Estas rutas manejan las solicitudes HTTP y utilizan los servicios definidos
# en services/credit_services.py para interactuar con la base de datos.
from flask import Blueprint, request, jsonify
from services.credit_services import (
    get_all_creditos,
    get_credito_by_id,
    create_credito,
    update_credito,
    delete_credito,
    get_statistics
)

# Definición del blueprint para las rutas API
api_bp = Blueprint('api', __name__)

# Ruta para obtener todos los créditos
@api_bp.route('/creditos', methods=['GET'])
def get_creditos():
    return jsonify([c.to_dict() for c in get_all_creditos()])

# Ruta para obtener un crédito por su ID
@api_bp.route('/creditos/<int:credito_id>', methods=['GET'])
def get_credito(credito_id):
    credito = get_credito_by_id(credito_id)
    return jsonify(credito.to_dict())

# Ruta para crear un nuevo crédito
@api_bp.route('/creditos', methods=['POST'])
def add_credito():
    data = request.json
    nuevo_credito = create_credito(data)
    return jsonify(nuevo_credito.to_dict()), 201

# Ruta para actualizar un crédito
@api_bp.route('/creditos/<int:credito_id>', methods=['PUT'])
def edit_credito(credito_id):
    data = request.json
    credito = update_credito(credito_id, data)
    return jsonify(credito.to_dict())

# Ruta para eliminar un crédito
@api_bp.route('/creditos/<int:credito_id>', methods=['DELETE'])
def delete_credit(credito_id):
    delete_credito(credito_id)
    return jsonify({'message': 'Crédito eliminado'}), 200

# Ruta para obtener estadísticas de los créditos
@api_bp.route('/creditos/statistics', methods=['GET'])
def credit_statistics():
    min_monto = request.args.get("min", type=float)
    max_monto = request.args.get("max", type=float)
    return jsonify(get_statistics(min_monto, max_monto))