import streamlit as st

from tfg.componentes.electrodomestico import Electrodomestico


class DisplayElectrodomestico:
    def __init__(self, electrodomestico: Electrodomestico) -> None:
        self.electrodomestico = electrodomestico
        self.toggle = False

    @property
    def consumo(self):
        return self.electrodomestico.potencia if self.toggle else 0

    def formatear_fila_componente(self):
        st.subheader(
            f"{self.electrodomestico.nombre} {iconos.get(self.electrodomestico.nombre, '⚡️')}"
        )
        self.toggle = st.toggle(
            "Activado", key=f"toggle_{self.electrodomestico.nombre}"
        )
        st.write(f"Consumo actual: {self.consumo} W.")


iconos = {
    "nevera": "❄️",
    "lavadora": "🧦",
}
