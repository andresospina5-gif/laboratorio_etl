import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import cartas_collection
from app.models.personajes_sql import Base, CartaPokemon

# Conexión MySQL
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/laboratorio_etl"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Crea la tabla si no existe
Base.metadata.create_all(engine)

def obtener_cartas(cantidad):
    try:
        cartas = []
        page = 1
        page_size = 250
        while len(cartas) < cantidad:
            response = requests.get(
                "https://api.pokemontcg.io/v2/cards",
                params={"page": page, "pageSize": page_size}
            )
            if response.status_code != 200:
                break
            data = response.json()["data"]
            if not data:
                break
            cartas.extend(data)
            page += 1
        return cartas[:cantidad]
    except Exception as e:
        print(f"Error obteniendo cartas: {e}")
        return []

def guardar_cartas_mongo(cartas):
    insertadas = 0
    for carta in cartas:
        carta["_id"] = carta["id"]
        resultado = cartas_collection.update_one(
            {"_id": carta["_id"]},
            {"$set": carta},
            upsert=True
        )
        if resultado.upserted_id:
            insertadas += 1
    return insertadas

def reset_mongo():
    resultado = cartas_collection.delete_many({})
    return resultado.deleted_count