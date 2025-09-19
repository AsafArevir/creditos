# Definición del modelo de datos para la entidad "Credito" usando SQLAlchemy
# para evitar inyecciones SQL y facilitar la manipulación de datos.
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Inicialización de la instancia de SQLAlchemy
db = SQLAlchemy()

# Definición del modelo Credito
class Credito(db.Model):
    __tablename__ = 'creditos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    tasa_interes = db.Column(db.Float, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    fecha_otorgamiento = db.Column(db.Date, nullable=False, default=date.today)
    
    # Método para convertir el objeto a un diccionario para facilitar su uso en JSON
    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'monto': self.monto,
            'tasa_interes': self.tasa_interes,
            'plazo': self.plazo,
            'fecha_otorgamiento': self.fecha_otorgamiento.strftime("%Y-%m-%d")
        }