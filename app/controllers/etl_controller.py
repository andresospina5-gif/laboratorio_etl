from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/etl",
    tags=["ETL"]
)

@router.get("/")
def prueba():
    return {
        "mensaje": "API funcionando"
    }