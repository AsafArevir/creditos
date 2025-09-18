# Datos de ejemplo para la base de datos de créditos.
# Este script inicializa la base de datos con algunos registros de ejemplo
# para facilitar las pruebas y el desarrollo.
from app import create_app
from models import db, Credito
from datetime import date

app = create_app()

with app.app_context():
    # Limpiar tabla
    db.drop_all()
    db.create_all()

    # Datos de ejemplo
    creditos = [
        Credito(cliente="Ana", monto=1200.50, tasa_interes=10.5, plazo=12, fecha_otorgamiento=date(2025, 1, 15)),
        Credito(cliente="Juan", monto=2500.00, tasa_interes=12.0, plazo=6, fecha_otorgamiento=date(2025, 3, 10)),
        Credito(cliente="Lucía", monto=1800.75, tasa_interes=11.0, plazo=9, fecha_otorgamiento=date(2025, 5, 20)),
        Credito(cliente="Pedro", monto=3000.00, tasa_interes=9.5, plazo=24, fecha_otorgamiento=date(2025, 7, 5)),
        Credito(cliente="Ana", monto=800.00, tasa_interes=13.0, plazo=4, fecha_otorgamiento=date(2025, 8, 30)),
    ]

    db.session.bulk_save_objects(creditos)
    db.session.commit()

    print("✅ Base de datos inicializada con datos de ejemplo.")