import datetime
from pathlib import Path

from tfg.componentes.electrodomestico import Electrodomestico
from tfg.componentes.vivienda import Vivienda


class TestVivienda:
    def test_can_calculate_consumption(self):
        vivienda = Vivienda(
            electrodomesticos=[
                Electrodomestico(
                    nombre="lavadora",
                    potencia=10,
                    tiempo_uso=datetime.timedelta(minutes=15),
                ),
                Electrodomestico(
                    nombre="nevera",
                    potencia=1,
                    tiempo_uso=datetime.timedelta(hours=5),
                ),
            ],
            paneles_solares=[],
            baterias=[],
        )
        assert vivienda.calcular_consumo() == 7.5

    def test_can_load_from_yaml(self, resources: Path):
        vivienda = Vivienda.from_config(resources / "vivienda_ejemplo.yml")

        assert len(vivienda.electrodomesticos) == 2
        assert len(vivienda.paneles_solares) == 1
        assert len(vivienda.baterias) == 2
