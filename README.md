# Laboratorio ETL — Pipeline con FastAPI

**Bases de Datos — Universidad de Antioquia**

## Descripción
Aplicación backend que orquesta un proceso ETL completo usando FastAPI, MongoDB y MySQL. Los datos son extraídos de la API pública de Pokémon TCG, almacenados en MongoDB como staging, transformados con Pandas y cargados en MySQL como Data Warehouse.

## Arquitectura

Pokémon TCG API → MongoDB (crudo) → Pandas (transformación) → MySQL (limpio)

## Diagrama ETL

[POST /extraer]  →  Descarga cartas de la API  →  Guarda en MongoDB
[POST /transformar]  →  Lee de MongoDB  →  Aplana con Pandas  →  Inserta en MySQL
[DELETE /reset]  →  Limpia MongoDB (delete_many)  →  Limpia MySQL (TRUNCATE)
[GET /analitica/columna/{nombre}]  →  Analiza columna de MySQL dinámicamente
[GET /perfil/{id}]  →  Cruza registro entre MongoDB y MySQL por ID

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/etl/extraer` | Extrae cartas de la API y guarda en MongoDB |
| POST | `/api/v1/etl/transformar` | Transforma datos de MongoDB y carga en MySQL |
| DELETE | `/api/v1/etl/reset` | Limpia MongoDB y MySQL |
| GET | `/api/v1/analitica/columna/{nombre}` | Análisis estadístico de una columna |
| GET | `/api/v1/perfil/{id}` | Perfil dual Mongo + SQL de una carta |

## Cómo ejecutar

1. Clonar el repositorio:
```bash
git clone https://github.com/andresospina5-gif/laboratorio_etl.git
cd laboratorio_etl
```

2. Crear el entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

5. Editar `.env` con tus credenciales locales.

6. Iniciar MongoDB (Windows):
```bash
mkdir C:\data\db
& "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe" --dbpath "C:\data\db"
```

7. Correr el servidor:
```bash
uvicorn app.main:app --reload
```

8. Abrir el navegador en: http://127.0.0.1:8000/docs

## Variables de entorno (.env)

| Variable | Descripción |
|----------|-------------|
| `MONGO_URI` | URI de conexión a MongoDB |
| `MYSQL_HOST` | Host de MySQL |
| `MYSQL_USER` | Usuario de MySQL |
| `MYSQL_PASSWORD` | Contraseña de MySQL |
| `MYSQL_DB` | Nombre de la base de datos |

## Estructura del proyecto

```
laboratorio_etl/
├── .env                    
├── .env.example            
├── .gitignore
├── requirements.txt
└── app/
    ├── main.py             
    ├── config.py
    ├── database.py         
    ├── controllers/
    │   ├── etl_controller.py
    │   └── analitica_controller.py
    ├── models/
    │   └── personajes_sql.py
    ├── services/
    │   ├── etl_service.py
    │   └── analitica_service.py
    └── views/
        ├── schemas.py
        └── analitica_schemas.py
```
## Cómo correr las pruebas de integración

1. Instalar dependencias de prueba:
```bash
pip install pytest httpx
```

2. Correr las pruebas:
```bash
pytest tests/
```

<!-- ## División de trabajo -->

| Integrante | Responsabilidad |
|------------|----------------|
| Andres Felipe Ospina Restrepo | Infraestructura, configuración FastAPI y MongoDB, Endpoint A `/extraer` |
| Yasleidy Palacios | Modelo SQLAlchemy, configuración MySQL, Endpoint B `/transformar` |
| Lorena Quintero | Endpoints analítica `/analitica/columna/{nombre}` y `/perfil/{id}` |
| Daniel Chavarria | Endpoint C `/reset`, README, requirements.txt, .gitignore, .env.example, pruebas de integración |