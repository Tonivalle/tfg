import yaml
from pydantic import BaseModel

from .electrodomestico import Electrodomestico


class Vivienda(BaseModel):
    electrodomesticos: list[Electrodomestico]

    def guardar_vivienda(self, archivo: str):
        with open(archivo, "w") as outfile:
            yaml.dump(self.model_dump(), outfile, default_flow_style=False)
