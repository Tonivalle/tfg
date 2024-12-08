from __future__ import annotations
from datetime import datetime
from tfg.componentes.paneles_solares import PanelSolar
import streamlit as st

class DisplayPanel:
    def __init__(self, panel:PanelSolar, irradiacion_adapter:IrradiacionAdapter) -> None:
        self.panel = panel
        self.irradiacion_adapter = irradiacion_adapter

    def calcular_generacion(self) -> float:
        """
        Calcula la energía generada total (W) mediante una serie de irradiacion por hora.
        """
        return self.panel.calcular_generacion_estimada_hora(self.irradiacion_adapter.irradiacion())

    def formatear_fila_componente(self, id:int):
        st.subheader(f"Panel Solar {id}")
        st.write(f"Generación actual: {self.calcular_generacion()} W.")

class IrradiacionAdapter:
    def irradiacion(self):
        return NotImplementedError
    
class MockIrradiacionAdapter(IrradiacionAdapter):
    def __init__(self) -> None:
        self.irradiacion_serie = {9:43,10: 188,11: 318,12: 394,13: 435,14: 410, 15:330, 16:205, 17:58}
    
    def irradiacion(self) -> int:
        return self.irradiacion_serie.get(datetime.now().hour, 0)
