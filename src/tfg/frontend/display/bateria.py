import datetime
from datetime import timedelta

import streamlit as st

from tfg.componentes.bateria import Bateria


class DisplayBateria:
    def __init__(self, bateria: Bateria, index: int = 0) -> None:
        self.bateria = bateria
        self.index = index

        self.session_key = f"bateria_{self.index}"

        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                "carga_actual": self.bateria.carga_actual,
                "ultimo_update": datetime.datetime.now(),
                "potencia_actual": 0.0,
            }
        else:
            self.bateria.carga_actual = st.session_state[self.session_key][
                "carga_actual"
            ]

    def actualizar_bateria_tiempo_real(self, potencia_asignada: float):
        """
        Actualiza la batería en tiempo real basada en la potencia asignada.
        """
        ahora = datetime.datetime.now()
        session_data = st.session_state[self.session_key]

        tiempo_transcurrido = ahora - session_data["ultimo_update"]
        horas = tiempo_transcurrido.total_seconds() / 3600

        if "potencia_actual" in session_data and horas > 0:
            cambio_carga = session_data["potencia_actual"] * horas
            nueva_carga = self.bateria.carga_actual + cambio_carga

            self.bateria.carga_actual = max(0, min(self.bateria.carga_max, nueva_carga))

            session_data["carga_actual"] = self.bateria.carga_actual

        session_data["ultimo_update"] = ahora
        session_data["potencia_actual"] = potencia_asignada

    def formatear_fila_componente(self, id: int, potencia_asignada: float = 0):
        self.actualizar_bateria_tiempo_real(potencia_asignada)

        st.subheader(f"Batería {id}: {self.bateria.carga_actual:.1f} Wh")
        texto = self._formatear_texto(potencia_asignada)
        st.progress(self.bateria.porcentaje, text=texto)

        st.session_state[self.session_key]["carga_actual"] = self.bateria.carga_actual

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🔋 Capacidad: {self.bateria.carga_max} Wh")
            st.write(f"📊 Porcentaje: {self.bateria.porcentaje:.1%}")
        with col2:
            if potencia_asignada > 0:
                st.write("🟢 **Cargando**")
                st.write(f"⚡ Potencia: +{potencia_asignada:.1f} W")
            elif potencia_asignada < 0:
                st.write("🔴 **Descargando**")
                st.write(f"⚡ Potencia: {potencia_asignada:.1f} W")
            else:
                st.write("⏸️ **En espera**")
                st.write("⚡ Potencia: 0 W")

    def _formatear_texto(self, potencia_actual: float) -> str:
        if self.bateria.esta_cargada:
            return "✅ Cargado por completo."

        if potencia_actual > 0:
            tiempo_carga = self.bateria.tiempo_hasta_carga_completa(potencia_actual)
            if tiempo_carga:
                return f"🔋 Cargando... {self._formatear_tiempo(tiempo_carga)} hasta carga completa"
            return "🔋 Cargando..."

        if potencia_actual < 0:
            tiempo_descarga = self.bateria.tiempo_hasta_descarga_completa(
                abs(potencia_actual)
            )
            if tiempo_descarga:
                return f"⚡ Descargando... {self._formatear_tiempo(tiempo_descarga)} hasta descarga"
            return "⚡ Descargando..."

        if self.bateria.esta_descargada:
            return "❌ Batería descargada."

        return "⏸️ Batería en espera."

    def _formatear_tiempo(self, tiempo: timedelta) -> str:
        """
        Formatea un timedelta a una cadena legible.
        """
        total_seconds = int(tiempo.total_seconds())
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        segundos = total_seconds % 60

        if horas > 0:
            return f"{horas:02d}h {minutos:02d}m {segundos:02d}s"
        elif minutos > 0:
            return f"{minutos:02d}m {segundos:02d}s"
        else:
            return f"{segundos:02d}s"
