import datetime

from pydantic import BaseModel


class Electrodomestico(BaseModel):
    nombre: str
    consumo_kwh: float
    tiempo_uso: datetime.time = datetime.time(hour=0, minute=0)
