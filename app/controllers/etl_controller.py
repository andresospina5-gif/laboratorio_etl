from fastapi import APIRouter
from app.views.schemas import ExtraccionRequest
from app.services.etl_service import (
    obtener_cartas,
    guardar_cartas_mongo,
    reset_mongo
)

router = APIRouter(
    prefix="/api/v1/etl",
    tags=["ETL"]
)

@router.get("/")
def prueba():
    return {
        "mensaje": "API funcionando"
    }

@router.post("/extraer")
def extraer(request: ExtraccionRequest):

    cartas = obtener_cartas(request.cantidad)

    insertadas = guardar_cartas_mongo(cartas)

    return {
        "cantidad_solicitada": request.cantidad,
        "cartas_obtenidas": len(cartas),
        "cartas_insertadas": insertadas
    }

@router.post("/reset")
def reset():

    eliminados = reset_mongo()

    return {
        "mensaje": "Coleccion reiniciada",
        "registros_eliminados": eliminados
    }