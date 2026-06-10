from fastapi import FastAPI
from app.controllers.etl_controller import router

app = FastAPI(
    title="Laboratorio ETL"
)

app.include_router(router)