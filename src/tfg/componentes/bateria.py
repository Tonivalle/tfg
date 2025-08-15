import datetime
from typing import Optional

from pydantic import BaseModel, PrivateAttr


class Bateria(BaseModel):
    carga_max: float
    carga_actual: float = 0
    
    _ultimo_update: Optional[datetime.datetime] = PrivateAttr(default=None)
    _potencia_actual: float = PrivateAttr(default=0.0)

    @property
    def porcentaje(self) -> float:
        return self.carga_actual / self.carga_max

    @property
    def esta_cargada(self) -> bool:
        """Devuelve True si la batería está al 100%"""
        return self.carga_actual >= self.carga_max

    @property
    def esta_descargada(self) -> bool:
        """Devuelve True si la batería está completamente descargada"""
        return self.carga_actual <= 0

    def actualizar_carga(self, potencia: float):
        """
        Actualiza la carga de la batería basado en la potencia actual.
        
        Args:
            potencia: Potencia en watts (positiva = carga, negativa = descarga)
        """
        ahora = datetime.datetime.now()
        
        if self._ultimo_update is not None:

            tiempo_transcurrido = ahora - self._ultimo_update
            horas = tiempo_transcurrido.total_seconds() / 3600
            
            cambio_carga = potencia * horas
            
            nueva_carga = self.carga_actual + cambio_carga
            
            self.carga_actual = max(0, min(self.carga_max, nueva_carga))
        
        self._ultimo_update = ahora
        self._potencia_actual = potencia

    def tiempo_hasta_carga_completa(self, potencia: float) -> Optional[datetime.timedelta]:
        """
        Calcula el tiempo hasta carga completa con la potencia dada.
        
        Args:
            potencia: Potencia de carga en watts (debe ser positiva)
            
        Returns:
            timedelta con el tiempo estimado, o None si ya está cargada o potencia <= 0
        """
        if potencia <= 0 or self.esta_cargada:
            return None
        
        carga_restante = self.carga_max - self.carga_actual
        horas = carga_restante / potencia
        return datetime.timedelta(hours=horas)

    def tiempo_hasta_descarga_completa(self, potencia: float) -> Optional[datetime.timedelta]:
        """
        Calcula el tiempo hasta descarga completa con la potencia dada.
        
        Args:
            potencia: Potencia de descarga en watts (debe ser positiva, representa consumo)
            
        Returns:
            timedelta con el tiempo estimado, o None si ya está descargada o potencia <= 0
        """
        if potencia <= 0 or self.esta_descargada:
            return None
        
        horas = self.carga_actual / potencia
        return datetime.timedelta(hours=horas)

    def puede_proporcionar_potencia(self, potencia: float) -> bool:
        """
        Verifica si la batería puede proporcionar la potencia solicitada.
        
        Args:
            potencia: Potencia solicitada en watts
            
        Returns:
            True si la batería tiene suficiente carga
        """
        return self.carga_actual > (potencia / 3600) and not self.esta_descargada

    def capacidad_carga_disponible(self) -> float:
        """
        Devuelve la capacidad de carga disponible en Wh.
        """
        return self.carga_max - self.carga_actual
