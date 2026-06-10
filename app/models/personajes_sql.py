from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
 
Base = declarative_base()
 
class CartaPokemon(Base):
    __tablename__ = "cartas_master"
 
    # PK alineada con _id de MongoDB (el id de la API, ej: "hgss4-1")
    id_carta      = Column(String(50), primary_key=True)
 
    nombre        = Column(String(200), nullable=False)
    supertype     = Column(String(50),  nullable=True)   # Pokémon, Trainer, Energy
    subtipo       = Column(String(100), nullable=True)   # Basic, Stage 1, Stage 2 …
    hp            = Column(Integer,     nullable=True)   # puede ser null en Trainer/Energy
    tipo_principal = Column(String(50), nullable=True)   # Fire, Water, Grass …
    rareza        = Column(String(100), nullable=True)   # Common, Rare Holo …
    nombre_set    = Column(String(200), nullable=True)
    serie         = Column(String(100), nullable=True)
    total_ataques = Column(Integer,     nullable=True)   # derivada: len(attacks[])
    artista       = Column(String(200), nullable=True)
    fecha_lanzamiento_set = Column(Date, nullable=True)  # de set.releaseDate "YYYY/MM/DD"