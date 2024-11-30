from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from .electrodomestico import Electrodomestico


class Vivienda(BaseModel):
    electrodomesticos: list[Electrodomestico]

    def calcular_consumo(self):
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
