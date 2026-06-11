from typing import Any, Dict, Optional
from pydantic import BaseModel


class AnaliticaColumnaResponse(BaseModel):
    columna: str
    tipo: str
    count: int
    distinct_count: int
    null_count: int
    mean: Optional[float] = None
    median: Optional[float] = None
    std: Optional[float] = None
    min: Optional[Any] = None
    max: Optional[Any] = None
    value_counts: Dict[str, int]


class PerfilResponse(BaseModel):
    vista_mongo: Dict[str, Any]
    vista_sql: Dict[str, Any]