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

any_active = any(
    st.session_state.get(f"electrodomestico_{e.nombre}", {}).get("activo", False)
    for e in vivienda.electrodomesticos
)

if any_active:
    time.sleep(1)
    st.rerun()
