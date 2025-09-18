# Herramienta de Registro de Créditos

Aplicación web para la gestión y visualización de créditos otorgados a clientes, desarrollada con **Flask** y **SQLAlchemy**.

---

## Instrucciones para ejecutar la aplicación

### 1. Clona el repositorio

```sh
git clone https://github.com/AsafArevir/creditos.git
```
#### Ingresar a la Carpeta

#### En Linux/Mac:

```sh
cd creditos
```

#### En Windows:

```sh
dir creditos
```

### 2. Crea y activa un entorno virtual

#### En Linux/Mac:

```sh
python -m venv venv
source venv/bin/activate
```

#### En Windows:

```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Instala las dependencias

Con requirements.txt:

```sh
pip install -r requirements.txt
```

O manualmente:

```sh
pip install flask flask-sqlalchemy
```

### 4. Ejecuta la aplicación

```sh
flask run
```

La aplicación estará disponible en [http://localhost:5000](http://localhost:5000)

> **Nota:** Debes contar con acceso a internet ya que la aplicación utiliza Chart.js y plugins desde CDN.

---

## Inicializar la base de datos con datos de ejemplo

Puedes ejecutar el script [`datos.py`](datos.py) para poblar la base de datos con registros de ejemplo:

```sh
python datos.py
```

---

## Características principales

- Registro, edición y eliminación de créditos.
- Visualización de créditos en tabla y gráfica por cliente.
- Filtros dinámicos por monto para la gráfica.
- Validaciones de formularios en frontend.
- Interfaz moderna y responsiva.
- API RESTful para operaciones CRUD y estadísticas.

---

## Estructura del proyecto

```
creditos/
│
├── app.py
├── datos.py
├── models.py
├── requirements.txt
├── README.md
│
├── db/
│   └── creditos.db
│
├── routes/
│   ├── api.py
│   └── views.py
│
├── services/
│   └── credit_services.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       └── validaciones.js
│
└── templates/
    ├── creditos.html
    ├── form_credito.html
    └── layout.html
```

---

## Módulos principales

- **app.py**: Configuración principal de Flask y registro de blueprints.
- **models.py**: Definición del modelo de datos `Credito`.
- **routes/api.py**: Rutas de la API REST para operaciones CRUD y estadísticas.
- **routes/views.py**: Rutas para renderizar vistas HTML.
- **services/credit_services.py**: Lógica de negocio y acceso a la base de datos.
- **datos.py**: Script para inicializar la base de datos con datos de ejemplo.
- **static/js/app.js**: Lógica de frontend para interacción con la API y la UI.
- **static/js/validaciones.js**: Validaciones de formularios en el frontend.
- **static/css/style.css**: Estilos CSS de la aplicación.
- **templates/**: Plantillas HTML para la interfaz de usuario.

---

## Notas importantes

- La base de datos SQLite se almacena en `db/creditos.db`.
- El frontend utiliza Chart.js y plugins desde CDN, por lo que se requiere conexión a internet.
- El sistema de validaciones previene errores comunes en la captura de datos.

---

## Licencia

MIT

---

Desarrollado por Asaf Diaz Rivera
