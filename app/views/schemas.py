from pydantic import BaseModel

class ExtraccionRequest(BaseModel):
    cantidad: int