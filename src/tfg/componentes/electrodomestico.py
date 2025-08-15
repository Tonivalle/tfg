import datetime
from typing import Optional

from pydantic import BaseModel, Field, PrivateAttr


class Electrodomestico(BaseModel):
    nombre: str
    potencia: float
    tiempo_uso: datetime.timedelta = Field(default_factory=lambda: datetime.timedelta(0))

    _inicio_uso: Optional[datetime.datetime] = PrivateAttr(default=None)
    _activo: bool = PrivateAttr(default=False)

    def calcular_consumo(self) -> float:
        return self.potencia * self._horas_uso()

    def _horas_uso(self) -> float:
        tiempo_total = self.get_tiempo_uso_total()
        return tiempo_total.total_seconds() / 3600

    def get_tiempo_uso_total(self) -> datetime.timedelta:
        """Obtiene el tiempo de uso total incluyendo el tiempo actual si está activo"""
        tiempo_acumulado = self.tiempo_uso
        
        if self._activo and self._inicio_uso:
            tiempo_actual = datetime.datetime.now() - self._inicio_uso
            tiempo_acumulado += tiempo_actual
            
        return tiempo_acumulado

    def iniciar_uso(self):
        """Inicia el contador de tiempo de uso"""
        if not self._activo:
            self._activo = True
            self._inicio_uso = datetime.datetime.now()

    def detener_uso(self):
        """Detiene el contador y acumula el tiempo transcurrido"""
        if self._activo and self._inicio_uso:
            tiempo_transcurrido = datetime.datetime.now() - self._inicio_uso
            self.tiempo_uso += tiempo_transcurrido
            self._activo = False
            self._inicio_uso = None

    @property
    def activo(self) -> bool:
        return self._activo
