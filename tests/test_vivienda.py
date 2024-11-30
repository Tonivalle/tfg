import datetime

from tfg.componentes.electrodomestico import Electrodomestico
from tfg.componentes.vivienda import Vivienda


class TestVivienda:
    def test_can_calculate_consumption(resources: str):
        vivienda = Vivienda(
            electrodomesticos=[
                Electrodomestico(
                    nombre="lavadora",
                    consumo_kwh=10,
                    tiempo_uso=datetime.time(hour=0, minute=15),
                ),
                Electrodomestico(
                    nombre="nevera",
                    consumo_kwh=1,
                    tiempo_uso=datetime.time(hour=5, minute=0),
                ),
            ]
        )
        assert vivienda.calcular_consumo() == 7.5

    def test_can_load_from_yaml(resources: str):
        vivienda = Vivienda.from_config("./resources/vivienda_ejemplo.yml")

        assert len(vivienda.electrodomesticos) == 2
