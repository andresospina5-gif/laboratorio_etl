from fastapi import APIRouter
from app.views.schemas import ExtraccionRequest

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
    return {
        "mensaje": "Extraccion recibida",
        "cantidad": request.cantidad
    }