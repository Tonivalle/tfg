from pathlib import Path
import time

import streamlit as st

from tfg.componentes.vivienda import Vivienda
from tfg.frontend.display.vivienda import DisplayVivienda

st.set_page_config(
    page_title="Paneles Solares",
    page_icon="",
)

st.title("Vivienda Solar")

vivienda = Vivienda.from_config(Path(__file__).parent.parent / "resources/vivienda.yml")

disp_vivienda = DisplayVivienda(vivienda)

disp_vivienda.display()

# Check if any appliance is active
any_active = any(
    st.session_state.get(f"electrodomestico_{e.nombre}", {}).get("activo", False)
    for e in vivienda.electrodomesticos
)

# Check if any battery is charging/discharging by looking at the current energy balance
generacion = sum(
    panel.calcular_generacion_estimada_hora(800)  # Using default irradiation
    for panel in vivienda.paneles_solares
)

consumo = sum(
    e.potencia if st.session_state.get(f"electrodomestico_{e.nombre}", {}).get("activo", False) else 0
    for e in vivienda.electrodomesticos
)

balance = generacion - consumo
any_battery_activity = abs(balance) > 0.1  # Small threshold to avoid float precision issues

if any_active or any_battery_activity:
    time.sleep(1)
    st.rerun()
