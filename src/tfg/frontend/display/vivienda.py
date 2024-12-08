import streamlit as st

from tfg.componentes.vivienda import Vivienda
from tfg.frontend.display.bateria import DisplayBateria
from tfg.frontend.display.electrodomestico import DisplayElectrodomestico
from tfg.frontend.display.panel_solar import DisplayPanel, MockIrradiacionAdapter


class DisplayVivienda:
    def __init__(self, vivienda: Vivienda) -> None:
        self.vivienda = vivienda
        self.dis_electrodomesticos = [
            DisplayElectrodomestico(electrodomestico)
            for electrodomestico in self.vivienda.electrodomesticos
        ]
        self.dis_paneles = [
            DisplayPanel(panel, MockIrradiacionAdapter())
            for panel in self.vivienda.paneles_solares
        ]
        self.dis_baterias = [
            DisplayBateria(bateria) for bateria in self.vivienda.baterias
        ]

    def display(self):
        self.display_paneles()
        self.display_electrodomesticos()
        self.display_baterias()

    def display_electrodomesticos(self):
        st.header(":orange[Electrodomésticos]", divider="orange")
        for dis_electrodomestico in self.dis_electrodomesticos:
            dis_electrodomestico.formatear_fila_componente()
        st.divider()
        st.markdown(f"##### Consumo Total: {self._consumo_actual()} W")
        st.divider()

    def display_paneles(self):
        st.header(":blue[Paneles Solares]", divider="blue")
        for idx, dis_paneles in enumerate(self.dis_paneles, 1):
            dis_paneles.formatear_fila_componente(idx)
        st.divider()
        st.markdown(f"##### Generación Total: {self._generacion_actual()} W")
        st.divider()

    def display_baterias(self):
        st.header(":green[Baterías]", divider="green")
        for idx, dis_bateria in enumerate(self.dis_baterias, 1):
            dis_bateria.formatear_fila_componente(
                id=idx,
                potencia_actual=(self._generacion_actual() - self._consumo_actual()),
            )
        st.divider()
        st.markdown(f"##### Batería Total: {self._carga_actual()} Wh")
        st.divider()

    def _consumo_actual(self) -> float:
        return sum(
            dis_electrodomestico.consumo
            for dis_electrodomestico in self.dis_electrodomesticos
        )

    def _generacion_actual(self) -> float:
        return sum(dis_panel.calcular_generacion() for dis_panel in self.dis_paneles)

    def _carga_actual(self) -> float:
        return sum(
            dis_bateria.bateria.carga_actual for dis_bateria in self.dis_baterias
        )
