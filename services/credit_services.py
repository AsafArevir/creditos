# Definición de servicios para manejar la lógica de negocio relacionada con créditos.
# Estos servicios interactúan con el modelo de datos y la base de datos.
from flask import abort, jsonify
from models import db, Credito
from sqlalchemy.sql import func
from datetime import date

# Función para obtener todos los créditos
def get_all_creditos():
    creditos = Credito.query.all()
    return creditos

# Función para obtener un crédito por su ID
def get_credito_by_id(credito_id):
    credito = db.session.get(Credito, credito_id)
    if not credito:
        abort(404)
    return credito

# Función para crear un nuevo crédito
def create_credito(data):
    fecha = data["fecha_otorgamiento"]
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha)

    nuevo_credito = Credito(
        cliente=data["cliente"],
        monto=data["monto"],
        tasa_interes=data["tasa_interes"],
        plazo=data["plazo"],
        fecha_otorgamiento=fecha,
    )
    db.session.add(nuevo_credito)
    db.session.commit()
    return nuevo_credito

# Función para actualizar un crédito
def update_credito(credito_id, data):
    credito = db.session.get(Credito, credito_id)
    if not credito:
        abort(404)
    fecha = data["fecha_otorgamiento"]
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha)
    credito.cliente = data.get("cliente", credito.cliente)
    credito.monto = data.get("monto", credito.monto)
    credito.tasa_interes = data.get("tasa_interes", credito.tasa_interes)
    credito.plazo = data.get("plazo", credito.plazo)
    credito.fecha_otorgamiento = fecha
    db.session.commit()
    return credito

# Función para eliminar un crédito
def delete_credito(credito_id):
    credito = db.session.get(Credito, credito_id)
    if not credito:
        abort(404)
    db.session.delete(credito)
    db.session.commit()
    return True

# Función para obtener estadísticas
def get_statistics(min_monto=None, max_monto=None):
    query = db.session.query(Credito)

    if min_monto is not None:
        query = query.filter(Credito.monto >= min_monto)
    if max_monto is not None:
        query = query.filter(Credito.monto <= max_monto)

    # calcular total en base a los filtros
    total = query.with_entities(func.sum(Credito.monto)).scalar() or 0
    total_count = query.with_entities(func.count(Credito.id)).scalar() or 0

    por_cliente = (
        query.with_entities(
            Credito.cliente, func.sum(Credito.monto), func.count(Credito.id)
        )
        .group_by(Credito.cliente)
        .all()
    )

    return {
        "total_monto": float(total),
        "total_count": total_count,
        "por_cliente": [
            {"cliente": c, "total": float(t or 0), "count": n}
            for c, t, n in por_cliente
        ],
    }
