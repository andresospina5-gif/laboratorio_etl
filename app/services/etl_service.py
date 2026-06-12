import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import cartas_collection
from app.models.personajes_sql import Base, CartaPokemon

# Conexión MySQL
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
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
    """Elimina todos los documentos de la colección MongoDB."""
    resultado = cartas_collection.delete_many({})
    return resultado.deleted_count

def _parse_fecha(fecha_str: str):
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y/%m/%d").date()
    except Exception:
        return None

def _parse_hp(hp_str):
    try:
        return int(hp_str)
    except (TypeError, ValueError):
        return None
    
 
def transformar_y_cargar():
    """
    Lee todos los documentos crudos de MongoDB,
    los aplana con Pandas e inserta en MySQL.
    Idempotente: usa INSERT ... ON DUPLICATE KEY UPDATE.
    """
 
    # 1. EXTRACT desde Mongo ──────────────────────
    documentos = list(cartas_collection.find())
    if not documentos:
        return 0
 
    # 2. TRANSFORM con Pandas ─────────────────────
    df = pd.DataFrame(documentos)
 
    # Columnas aplanadas que necesitamos
    df["id_carta"]      = df["id"].fillna("N/A")
    df["nombre"]        = df["name"].fillna("N/A")
    df["supertype"]     = df.get("supertype", pd.Series(dtype=str)).fillna("N/A")
 
    # subtipo: primer elemento de la lista subtypes[]
    df["subtipo"] = df["subtypes"].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "N/A"
    )
 
    # hp viene como string en la API
    df["hp"] = df["hp"].apply(_parse_hp)
 
    # tipo_principal: primer elemento de types[]
    df["tipo_principal"] = df["types"].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "N/A"
    )
 
    df["rareza"]      = df.get("rarity", pd.Series(dtype=str)).fillna("N/A")
 
    # Campos anidados de set{}
    df["nombre_set"]  = df["set"].apply(
        lambda x: x.get("name", "N/A") if isinstance(x, dict) else "N/A"
    )
    df["serie"] = df["set"].apply(
        lambda x: x.get("series", "N/A") if isinstance(x, dict) else "N/A"
    )
    df["fecha_lanzamiento_set"] = df["set"].apply(
        lambda x: _parse_fecha(x.get("releaseDate")) if isinstance(x, dict) else None
    )
 
    # total_ataques: derivada de attacks[]
    df["total_ataques"] = df["attacks"].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )
 
    df["artista"] = df.get("artist", pd.Series(dtype=str)).fillna("N/A")
 
    # Seleccionar solo las columnas finales
    columnas_finales = [
        "id_carta", "nombre", "supertype", "subtipo", "hp",
        "tipo_principal", "rareza", "nombre_set", "serie",
        "total_ataques", "artista", "fecha_lanzamiento_set"
    ]
    df_final = df[columnas_finales].copy()
 
    # 3. LOAD en MySQL ────────────────────────────
    # Idempotencia via INSERT ... ON DUPLICATE KEY UPDATE
    insertados = 0
    session = SessionLocal()
    try:
        for _, row in df_final.iterrows():
            sql = text("""
                INSERT INTO cartas_master
                    (id_carta, nombre, supertype, subtipo, hp,
                     tipo_principal, rareza, nombre_set, serie,
                     total_ataques, artista, fecha_lanzamiento_set)
                VALUES
                    (:id_carta, :nombre, :supertype, :subtipo, :hp,
                     :tipo_principal, :rareza, :nombre_set, :serie,
                     :total_ataques, :artista, :fecha_lanzamiento_set)
                ON DUPLICATE KEY UPDATE
                    nombre               = VALUES(nombre),
                    supertype            = VALUES(supertype),
                    subtipo              = VALUES(subtipo),
                    hp                   = VALUES(hp),
                    tipo_principal       = VALUES(tipo_principal),
                    rareza               = VALUES(rareza),
                    nombre_set           = VALUES(nombre_set),
                    serie                = VALUES(serie),
                    total_ataques        = VALUES(total_ataques),
                    artista              = VALUES(artista),
                    fecha_lanzamiento_set = VALUES(fecha_lanzamiento_set)
            """)
            result = session.execute(sql, row.to_dict())
            # rowcount == 1 → INSERT nuevo; == 2 → UPDATE existente
            if result.rowcount == 1:
                insertados += 1
 
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error al cargar en MySQL: {e}")
        raise e
    finally:
        session.close()
 
    return len(df_final)   # total procesados

def reset_mysql():
    """Vacía la tabla con TRUNCATE (no DROP) y retorna filas eliminadas."""
    session = SessionLocal()
    try:
        # Contar antes de borrar
        count_result = session.execute(text("SELECT COUNT(*) FROM cartas_master"))
        total = count_result.scalar()
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        session.execute(text("TRUNCATE TABLE cartas_master"))
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        session.commit()
        return total
    except Exception as e:
        session.rollback()
        print(f"Error en reset MySQL: {e}")
        raise e
    finally:
        session.close()
 