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
            DisplayBateria(bateria, index)
            for index, bateria in enumerate(self.vivienda.baterias)
        ]

    def display(self):
        self.display_balance_energetico()
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

    def display_balance_energetico(self):
        """Muestra el balance energético del sistema"""
        st.header(":violet[Balance Energético]", divider="violet")

        generacion = self._generacion_actual()
        consumo = self._consumo_actual()
        balance = generacion - consumo

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🌞 Generación",
                f"{generacion:.1f} W",
                help="Energía generada por paneles solares",
            )

        with col2:
            st.metric(
                "⚡ Consumo",
                f"{consumo:.1f} W",
                help="Energía consumida por electrodomésticos",
            )

        with col3:
            if balance > 0:
                st.metric(
                    "🔋 Balance",
                    f"+{balance:.1f} W",
                    help="Exceso de energía - Las baterías se cargan",
                    delta="Exceso",
                )
            elif balance < 0:
                st.metric(
                    "🔋 Balance",
                    f"{balance:.1f} W",
                    help="Déficit de energía - Las baterías se descargan",
                    delta="-Déficit",
                )
            else:
                st.metric("🔋 Balance", "0 W", help="Equilibrio perfecto", delta=None)

        st.divider()

    def display_baterias(self):
        st.header(":green[Baterías]", divider="green")

        generacion = self._generacion_actual()
        consumo = self._consumo_actual()
        balance = generacion - consumo

        if len(self.dis_baterias) > 0:
            if balance > 0:
                if baterias_disponibles := [
                    (i, dis_bateria)
                    for i, dis_bateria in enumerate(self.dis_baterias)
                    if not dis_bateria.bateria.esta_cargada
                ]:
                    potencia_por_bateria = balance / len(baterias_disponibles)
                    for i, dis_bateria in enumerate(self.dis_baterias, 1):
                        if not dis_bateria.bateria.esta_cargada:
                            dis_bateria.formatear_fila_componente(
                                id=i,
                                potencia_asignada=potencia_por_bateria,
                            )
                        else:
                            dis_bateria.formatear_fila_componente(
                                id=i,
                                potencia_asignada=0,
                            )
                else:
                    for i, dis_bateria in enumerate(self.dis_baterias, 1):
                        dis_bateria.formatear_fila_componente(id=i, potencia_asignada=0)

            elif balance < 0:
                if baterias_disponibles := [
                    (i, dis_bateria)
                    for i, dis_bateria in enumerate(self.dis_baterias)
                    if dis_bateria.bateria.carga_actual > 0
                ]:
                    potencia_por_bateria = balance / len(baterias_disponibles)
                    for i, dis_bateria in enumerate(self.dis_baterias, 1):
                        if dis_bateria.bateria.carga_actual > 0:
                            dis_bateria.formatear_fila_componente(
                                id=i,
                                potencia_asignada=potencia_por_bateria,
                            )
                        else:
                            dis_bateria.formatear_fila_componente(
                                id=i,
                                potencia_asignada=0,
                            )
                else:
                    for i, dis_bateria in enumerate(self.dis_baterias, 1):
                        dis_bateria.formatear_fila_componente(id=i, potencia_asignada=0)

            else:
                for i, dis_bateria in enumerate(self.dis_baterias, 1):
                    dis_bateria.formatear_fila_componente(id=i, potencia_asignada=0)

        st.divider()

        carga_total = self._carga_actual()
        capacidad_total = sum(bateria.carga_max for bateria in self.vivienda.baterias)
        porcentaje_total = (carga_total / capacidad_total) if capacidad_total > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔋 Carga Total", f"{carga_total:.1f} Wh")
        with col2:
            st.metric("📊 Capacidad Total", f"{capacidad_total:.1f} Wh")
        with col3:
            st.metric("📈 Porcentaje Total", f"{porcentaje_total:.1%}")

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
