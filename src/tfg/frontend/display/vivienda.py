from tfg.componentes.vivienda import Vivienda
from tfg.frontend.display.electrodomestico import DisplayElectrodomestico
import streamlit as st

class DisplayVivienda:
    def __init__(self, vivienda:Vivienda) -> None:
        self.vivienda = vivienda
        self.dis_electrodomesticos = [DisplayElectrodomestico(electrodomestico) for electrodomestico in self.vivienda.electrodomesticos]
    
    def display(self):
        self.display_electrodomesticos()

    def display_electrodomesticos(self):
        st.header(":orange[Electrodomésticos]", divider="orange")
        for dis_electrodomestico in self.dis_electrodomesticos:
            dis_electrodomestico.formatear_fila_componente()
        st.divider()
        st.markdown(f'#### Consumo Total: {self._consumo_actual()} kWh')
        
    def _consumo_actual(self) -> float:
        return sum(dis_electrodomestico.consumo for dis_electrodomestico in self.dis_electrodomesticos)