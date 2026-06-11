from fastapi import APIRouter, HTTPException
from app.services.analitica_service import obtener_analisis_columna, obtener_perfil_por_id
from app.views.analitica_schemas import AnaliticaColumnaResponse, PerfilResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["Analítica"]
)

@router.get("/analitica/columna/{nombre}", response_model=AnaliticaColumnaResponse)
def analisis_columna(nombre: str):
    try:
        return obtener_analisis_columna(nombre)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al calcular la analítica")

@router.get("/perfil/{id}", response_model=PerfilResponse)
def perfil(id: str):
    try:
        return obtener_perfil_por_id(id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al consultar el perfil")