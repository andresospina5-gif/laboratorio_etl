from fastapi import APIRouter
from app.views.schemas import ExtraccionRequest
from app.services.etl_service import (
    obtener_cartas,
    guardar_cartas_mongo,
    reset_mongo,
    transformar_y_cargar,
    reset_mysql,
)

router = APIRouter(
    prefix="/api/v1/etl",
    tags=["ETL"]
)

@router.get("/")
def prueba():
    return {"mensaje": "API funcionando"}
@router.post("/extraer", status_code=201)
def extraer(request: ExtraccionRequest):
    if request.cantidad <= 0:
        return {"error": "La cantidad debe ser mayor que cero"}
    cartas = obtener_cartas(request.cantidad)
    insertadas = guardar_cartas_mongo(cartas)
    return {
        "mensaje": "Datos extraídos exitosamente",
        "registros_guardados": insertadas,
        "fuente": "Pokémon TCG API",
        "status": 201
    }
# ── Endpoint B: Transformación y Carga ───────────────────────────────────────
@router.post("/transformar", status_code=200)
def transformar():
    total_procesados = transformar_y_cargar()
    return {
        "mensaje": "Pipeline finalizado",
        "registros_procesados": total_procesados,
        "tabla_destino": "cartas_master",
        "status": 200
    }
# ── Endpoint C: Reset ─────────────────────────────────────────────────────────
@router.delete("/reset", status_code=200)
def reset():
    mongo_eliminados = reset_mongo()
    mysql_eliminadas = reset_mysql()
    return {
        "mensaje": "Sistema reseteado correctamente",
        "mongo_docs_eliminados": mongo_eliminados,
        "mysql_rows_eliminadas": mysql_eliminadas,
        "status": 200
    }
