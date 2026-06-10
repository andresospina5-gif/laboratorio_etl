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
