from datetime import datetime, timedelta
import streamlit as st
from tfg.componentes.bateria import Bateria


class DisplayBateria:
    def __init__(self, bateria: Bateria) -> None:
        self.bateria = bateria

    def formatear_fila_componente(self, id: int, potencia_actual:float=0):
        st.subheader(f"Batería {id}: {self.bateria.carga_actual} Wh")
        texto = self._formatear_texto(potencia_actual)
        st.progress(self.bateria.porcentaje, text=texto)
    
    def _formatear_texto(self, potencia_actual:float)->str:
        if self.bateria.porcentaje == 1:
            return "Cargado por completo."
        if potencia_actual > 0:
            return f"Cargando... Tiempo hasta carga completa: {self._estimar_tiempo_carga(potencia_actual)}" # TODO: si se tienen multiples baterías, la potencia se debería dividir entre ellas.
        if potencia_actual < 0:
            return f"Consumiendo energía. Tiempo hasta descarga: {self._estimar_tiempo_descarga(potencia_actual)}"
        return "Batería en espera." 
    
    def calcular_reservas(self) -> float:
        return self.bateria.porcentaje
    
    def _estimar_tiempo_carga(self, potencia: float) -> float: # TODO Mover al componente batería
        """
        Ecuación: Tiempo carga (h) = Capacidad batería restante (Wh) / Potencia Carga (W)
        """
        if potencia > 0:
            return _formatear_horas_a_string((self.bateria.carga_max - self.bateria.carga_actual) / potencia)
        raise ValueError("Potencia debe ser mayor que 0.")
    
    def _estimar_tiempo_descarga(self, potencia: float) -> float: # TODO Mover al componente batería
        """
        Ecuación: Tiempo descarga (h) = Capacidad actual (Wh) / Potencia Carga (W)
        """
        if potencia < 0:
            return  _formatear_horas_a_string(self.bateria.carga_actual / - potencia)
        raise ValueError("Potencia debe ser menor que 0.")
    
def _formatear_horas_a_string(horas: float) -> datetime:
    """
    Formateamos a formato timedelta.

    Le restamos los microsegundos para simplificar la lectura.
    """
    return timedelta(hours=horas) - timedelta(microseconds= timedelta(hours=horas).microseconds)
