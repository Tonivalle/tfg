import datetime

import streamlit as st

from tfg.componentes.electrodomestico import Electrodomestico


class DisplayElectrodomestico:
    def __init__(self, electrodomestico: Electrodomestico) -> None:
        self.electrodomestico = electrodomestico
        self._set_session_key()

    def _set_session_key(self):
        self.session_key = f"electrodomestico_{self.electrodomestico.nombre}"

        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                "tiempo_acumulado": datetime.timedelta(0),
                "inicio_uso": None,
                "activo": False,
            }

    @property
    def consumo(self):
        return self.electrodomestico.potencia if self._esta_activado() else 0

    def _esta_activado(self):
        return st.session_state[self.session_key]["activo"]

    def _get_tiempo_total(self):
        session_data = st.session_state[self.session_key]
        tiempo_acumulado = session_data["tiempo_acumulado"]

        if session_data["activo"] and session_data["inicio_uso"]:
            tiempo_actual = datetime.datetime.now() - session_data["inicio_uso"]
            return tiempo_acumulado + tiempo_actual

        return tiempo_acumulado

    def formatear_fila_componente(self):
        st.subheader(
            f"{self.electrodomestico.nombre} {iconos.get(self.electrodomestico.nombre, '⚡️')}"
        )

        estado_toggle = st.toggle(
            "Activado",
            value=self._esta_activado(),
            key=f"toggle_{self.electrodomestico.nombre}",
        )

        self._actualizar_tiempo_uso(estado_toggle)

        st.write(f"Consumo actual: {self.consumo} W.")

        horas, minutos, segundos = self._obtener_tiempo_uso()

        st.write(f"Tiempo de uso total: {horas:02d}:{minutos:02d}:{segundos:02d}")

    def _actualizar_tiempo_uso(self, estado_toggle):
        if estado_toggle != self._esta_activado():
            if estado_toggle:
                # Iniciar uso
                st.session_state[self.session_key]["activo"] = True
                st.session_state[self.session_key]["inicio_uso"] = (
                    datetime.datetime.now()
                )
            else:
                # Detener uso y acumular tiempo
                if (
                    st.session_state[self.session_key]["activo"]
                    and st.session_state[self.session_key]["inicio_uso"]
                ):
                    tiempo_transcurrido = (
                        datetime.datetime.now()
                        - st.session_state[self.session_key]["inicio_uso"]
                    )
                    st.session_state[self.session_key]["tiempo_acumulado"] += (
                        tiempo_transcurrido
                    )

                st.session_state[self.session_key]["activo"] = False
                st.session_state[self.session_key]["inicio_uso"] = None

    def _obtener_tiempo_uso(self):
        tiempo_total = self._get_tiempo_total()
        horas = int(tiempo_total.total_seconds() // 3600)
        minutos = int((tiempo_total.total_seconds() % 3600) // 60)
        segundos = int(tiempo_total.total_seconds() % 60)
        return horas, minutos, segundos


iconos = {
    "nevera": "❄️",
    "lavadora": "🧦",
}
