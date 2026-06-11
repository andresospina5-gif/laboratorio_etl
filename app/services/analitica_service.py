import re
import pandas as pd
from typing import Any, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import cartas_collection
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def _es_nombre_columna_valido(nombre: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", nombre))


def detectar_tipo_serie(serie: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(serie):
        return "booleana"
    if pd.api.types.is_numeric_dtype(serie):
        return "numérica"
    try:
        pd.to_datetime(serie, errors="raise")
        return "fecha"
    except Exception:
        pass
    return "categorica"


def distinct_count(serie: pd.Series) -> int:
    return int(serie.nunique())


def null_count(serie: pd.Series) -> int:
    return int(serie.isna().sum())


def value_counts(serie: pd.Series) -> Dict[str, int]:
    return {str(k): int(v) for k, v in serie.value_counts().items()}


def calcular_range_numerico(serie: pd.Series) -> Dict[str, Any]:
    return {
        "mean": round(float(serie.mean()), 2),
        "median": round(float(serie.median()), 2),
        "std": round(float(serie.std()), 2),
        "min": float(serie.min()),
        "max": float(serie.max()),
    }


def calcular_range_fecha(serie: pd.Series) -> Dict[str, Any]:
    fechas = pd.to_datetime(serie, errors="coerce")
    return {
        "min": str(fechas.min().date()),
        "max": str(fechas.max().date()),
    }


def obtener_analisis_columna(nombre: str):
    if not _es_nombre_columna_valido(nombre):
        raise ValueError(f"Columna '{nombre}' no es válida para análisis")

    session = SessionLocal()
    try:
        query = text(f"SELECT * FROM cartas_master WHERE {nombre} IS NOT NULL")
        result = session.execute(query)
        rows = result.mappings().all()
        df = pd.DataFrame(rows)
    finally:
        session.close()

    if df.empty or nombre not in df.columns:
        raise ValueError(f"Columna '{nombre}' no existe o no tiene datos")

    serie = df[nombre]
    tipo = detectar_tipo_serie(serie)
    output = {
        "columna": nombre,
        "tipo": tipo,
        "count": int(serie.count()),
        "distinct_count": distinct_count(serie),
        "null_count": null_count(serie),
        "value_counts": value_counts(serie)
    }

    if tipo == "numérica":
        output.update(calcular_range_numerico(pd.to_numeric(serie, errors="coerce")))
    elif tipo == "fecha":
        output.update(calcular_range_fecha(serie))
    else:
        output.update({"mean": None, "median": None, "std": None, "min": None, "max": None})

    return output


def obtener_perfil_por_id(id_valor: str) -> Dict[str, Any]:
    documento = cartas_collection.find_one({"_id": id_valor})
    vista_mongo = {} if documento is None else {k: v for k, v in documento.items() if k != "_id"}

    session = SessionLocal()
    try:
        query = text("SELECT * FROM cartas_master WHERE id_carta = :id")
        result = session.execute(query, {"id": id_valor}).mappings().all()
        vista_sql = dict(result[0]) if result else {}
    finally:
        session.close()

    if not vista_mongo and not vista_sql:
        raise ValueError(f"Perfil '{id_valor}' no encontrado")

    return {"vista_mongo": vista_mongo, "vista_sql": vista_sql}