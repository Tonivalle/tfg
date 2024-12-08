from tfg.componentes.vivienda import Vivienda
from tfg.frontend.display.electrodomestico import DisplayElectrodomestico
import streamlit as st

from tfg.frontend.display.paneles_solares import DisplayPanel, MockIrradiacionAdapter

class DisplayVivienda:
    def __init__(self, vivienda:Vivienda) -> None:
        self.vivienda = vivienda
        self.dis_electrodomesticos = [DisplayElectrodomestico(electrodomestico) for electrodomestico in self.vivienda.electrodomesticos]
        self.dis_paneles = [DisplayPanel(panel, MockIrradiacionAdapter()) for panel in self.vivienda.paneles_solares]

    def display(self):
        self.display_paneles()
        self.display_electrodomesticos()

    def display_electrodomesticos(self):
        st.header(":orange[Electrodomésticos]", divider="orange")
        for dis_electrodomestico in self.dis_electrodomesticos:
            dis_electrodomestico.formatear_fila_componente()
        st.divider()
        st.markdown(f'#### Consumo Total: {self._consumo_actual()} kWh')

    def display_paneles(self):
        st.header(":blue[Paneles Solares]", divider="blue")
        for idx, dis_paneles in enumerate(self.dis_paneles):
            dis_paneles.formatear_fila_componente(idx)
        st.divider()
        st.markdown(f'#### Generación Total: {self._generacion_actual()} kWh')

    def _consumo_actual(self) -> float:
        return sum(dis_electrodomestico.consumo for dis_electrodomestico in self.dis_electrodomesticos)
    
    def _generacion_actual(self) -> float:
        return sum(dis_panel.calcular_generacion() for dis_panel in self.dis_paneles)
    