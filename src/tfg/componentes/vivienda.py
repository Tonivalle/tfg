from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import yaml
from pydantic import BaseModel

from tfg.componentes.bateria import Bateria
from tfg.componentes.electrodomestico import Electrodomestico
from tfg.componentes.panel_solar import PanelSolar


class Vivienda(BaseModel):
    electrodomesticos: list[Electrodomestico]
    paneles_solares: list[PanelSolar]
    baterias: list[Bateria]

    def calcular_consumo(self) -> float:
        return sum(
            electrodomestico.calcular_consumo()
            for electrodomestico in self.electrodomesticos
        )

    def calcular_generacion_solar(self, irradiacion: float = 800) -> float:
        """
        Calcula la generación total de los paneles solares.

        Args:
            irradiacion: Irradiación solar en W/m² (por defecto 800)
        """
        return sum(
            panel.calcular_generacion_estimada_hora(irradiacion)
            for panel in self.paneles_solares
        )

    def calcular_balance_energetico(self, irradiacion: float = 800) -> float:
        """
        Calcula el balance energético (generación - consumo).
        Positivo = exceso de energía, Negativo = déficit de energía
        """
        generacion = self.calcular_generacion_solar(irradiacion)
        consumo = self.calcular_consumo_instantaneo()
        return generacion - consumo

    def calcular_consumo_instantaneo(self) -> float:
        """
        Calcula el consumo instantáneo basado en electrodomésticos activos.

        Para esto necesitamos acceder al estado actual desde la sesión de Streamlit
        ya que el estado activo se mantiene en el DisplayElectrodomestico.
        """
        return sum(
            electrodomestico.potencia
            if getattr(electrodomestico, "_activo", False)
            else 0
            for electrodomestico in self.electrodomesticos
        )

    def distribuir_potencia_baterias(
        self, potencia_neta: float
    ) -> List[Tuple[Bateria, float]]:
        """
        Distribuye la potencia entre las baterías de manera inteligente.

        Args:
            potencia_neta: Potencia neta disponible (+ = exceso, - = déficit)

        Returns:
            Lista de tuplas (bateria, potencia_asignada)
        """
        distribucion = []

        if potencia_neta > 0:
            if baterias_disponibles := [b for b in self.baterias if not b.esta_cargada]:
                capacidades_disponibles = [
                    b.capacidad_carga_disponible() for b in baterias_disponibles
                ]
                total_capacidad = sum(capacidades_disponibles)

                if total_capacidad > 0:
                    for bateria, capacidad in zip(
                        baterias_disponibles, capacidades_disponibles
                    ):
                        proporcion = capacidad / total_capacidad
                        potencia_asignada = potencia_neta * proporcion
                        distribucion.append((bateria, potencia_asignada))
                        bateria.actualizar_carga(potencia_asignada)

        elif potencia_neta < 0:
            if baterias_disponibles := [
                b
                for b in self.baterias
                if b.puede_proporcionar_potencia(abs(potencia_neta))
            ]:
                cargas_actuales = [b.carga_actual for b in baterias_disponibles]
                total_carga = sum(cargas_actuales)

                if total_carga > 0:
                    for bateria, carga in zip(baterias_disponibles, cargas_actuales):
                        proporcion = carga / total_carga
                        potencia_asignada = potencia_neta * proporcion
                        distribucion.append((bateria, potencia_asignada))
                        bateria.actualizar_carga(potencia_asignada)

        return distribucion

    def actualizar_sistema_baterias(self, irradiacion: float = 800):
        """
        Actualiza todo el sistema de baterías basado en el balance energético actual.
        """
        balance = self.calcular_balance_energetico(irradiacion)
        return self.distribuir_potencia_baterias(balance)

    def guardar_vivienda(self, archivo: str):
        with open(archivo, "w") as outfile:
            yaml.dump(self.model_dump(), outfile, default_flow_style=False)

    @classmethod
    def from_config(cls, ruta: Path | str) -> Vivienda:
        with open(ruta, "r") as archivo:
            atributos = yaml.load(archivo, Loader=yaml.SafeLoader)
        return cls(**atributos)
