from fastapi import APIRouter
from app.views.schemas import ExtraccionRequest
from app.services.etl_service import obtener_cartas

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

    return {
        "mensaje": "Extraccion recibida",
        "cantidad_solicitada": request.cantidad,
        "cartas_obtenidas": len(cartas)
    }