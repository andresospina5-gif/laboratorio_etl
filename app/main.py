from fastapi import FastAPI
from app.controllers.etl_controller import router as etl_router
from app.controllers.analitica_controller import router as analitica_router

app = FastAPI(
    title="Laboratorio ETL"
)

app.include_router(etl_router)
app.include_router(analitica_router)