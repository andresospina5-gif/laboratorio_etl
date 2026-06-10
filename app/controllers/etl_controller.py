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
