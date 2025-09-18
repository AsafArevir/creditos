# Definición de servicios para manejar la lógica de negocio relacionada con créditos.
# Estos servicios interactúan con el modelo de datos y la base de datos.
from flask import jsonify
from models import db, Credito
from sqlalchemy.sql import func
from datetime import date


def get_all_creditos():
    # Obtiene todos los créditos de la base de datos.
    creditos = Credito.query.all()
    return creditos


def get_credito_by_id(credito_id):
    # Obtiene un crédito por su ID.
    return Credito.query.get_or_404(credito_id)


def create_credito(data):
    # Crea un nuevo crédito en la base de datos.
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


def update_credito(credito_id, data):
    # Actualiza un crédito existente.
    credito = Credito.query.get_or_404(credito_id)
    credito.cliente = data.get("cliente", credito.cliente)
    credito.monto = data.get("monto", credito.monto)
    credito.tasa_interes = data.get("tasa_interes", credito.tasa_interes)
    credito.plazo = data.get("plazo", credito.plazo)
    db.session.commit()
    return credito


def delete_credito(credito_id):
    # Elimina un crédito de la base de datos.
    credito = Credito.query.get_or_404(credito_id)
    db.session.delete(credito)
    db.session.commit()
    return True


# def get_statistics():
#     # Obtiene estadísticas resumidas de los créditos.
#     total = db.session.query(func.sum(Credito.monto)).scalar() or 0
#     por_cliente = (
#         db.session.query(Credito.cliente, func.sum(Credito.monto))
#         .group_by(Credito.cliente).all()
#     )
#     return {
#         "total": total,
#         "por_cliente": [{"cliente": c, "total": t} for c, t in por_cliente]
#     }


def get_statistics(min_monto=None, max_monto=None):
    query = db.session.query(Credito)

    if min_monto is not None:
        query = query.filter(Credito.monto >= min_monto)
    if max_monto is not None:
        query = query.filter(Credito.monto <= max_monto)

    # calcular total respetando filtros
    total = query.with_entities(func.sum(Credito.monto)).scalar() or 0
    total_count = query.with_entities(func.count(Credito.id)).scalar() or 0 

    por_cliente = (
        query.with_entities(
            Credito.cliente,
            func.sum(Credito.monto),
            func.count(Credito.id)
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
        ]
    }
