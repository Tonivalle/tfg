import datetime

from tfg.componentes.electrodomestico import Electrodomestico


class TestElectrodomestico:
    def test_can_calculate_consumption(self):
        electrodomestico = Electrodomestico(
            nombre="lavadora",
            consumo_kwh=10,
            tiempo_uso=datetime.time(hour=0, minute=15),
        )
        assert electrodomestico.calcular_consumo() == 2.5
