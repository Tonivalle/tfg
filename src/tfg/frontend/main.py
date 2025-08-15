import time
from pathlib import Path

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

time.sleep(1)
st.rerun()
