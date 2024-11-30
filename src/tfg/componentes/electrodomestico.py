import datetime

from pydantic import BaseModel


class Electrodomestico(BaseModel):
    nombre: str
    consumo_kwh: float
    tiempo_uso: datetime.time = datetime.time(hour=0, minute=0)

    def calcular_consumo(self) -> float:
        return self.consumo_kwh * self._horas_uso()

    def _horas_uso(self) -> float:
        return (
            self.tiempo_uso.hour
            + (self.tiempo_uso.minute / 60)
            + (self.tiempo_uso.second / 3600)
        )
