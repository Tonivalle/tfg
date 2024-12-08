import datetime

from pydantic import BaseModel


class Bateria(BaseModel):
    carga_max: float
    carga_actual: float = 0
    
    @property
    def porcentaje(self) -> float:
        return self.carga_actual / self.carga_max