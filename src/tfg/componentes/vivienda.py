from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from tfg.componentes.baterias import Bateria
from tfg.componentes.paneles_solares import PanelSolar

from .electrodomestico import Electrodomestico


class Vivienda(BaseModel):
    electrodomesticos: list[Electrodomestico]
    paneles_solares: list[PanelSolar]
    baterias: list[Bateria]

    def calcular_consumo(self) -> float:
        return sum(
            electrodomestico.calcular_consumo()
            for electrodomestico in self.electrodomesticos
        )

    def guardar_vivienda(self, archivo: str):
        with open(archivo, "w") as outfile:
            yaml.dump(self.model_dump(), outfile, default_flow_style=False)

    @classmethod
    def from_config(cls, ruta: Path | str) -> Vivienda:
        with open(ruta, "r") as archivo:
            atributos = yaml.load(archivo, Loader=yaml.SafeLoader)
        return cls(**atributos)
