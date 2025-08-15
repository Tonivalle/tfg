import datetime

from tfg.componentes.electrodomestico import Electrodomestico


class TestElectrodomestico:
    def test_can_calculate_consumption(self):
        electrodomestico = Electrodomestico(
            nombre="lavadora",
            potencia=10,
            tiempo_uso=datetime.timedelta(minutes=15),
        )
        assert electrodomestico.calcular_consumo() == 2.5

    def test_can_start_and_stop_usage_tracking(self):
        electrodomestico = Electrodomestico(
            nombre="lavadora",
            potencia=10,
        )
        
        assert not electrodomestico.activo
        assert electrodomestico.get_tiempo_uso_total() == datetime.timedelta(0)
        
        electrodomestico.iniciar_uso()
        assert electrodomestico.activo
        
        electrodomestico.detener_uso()
        assert not electrodomestico.activo
        
        assert electrodomestico.tiempo_uso > datetime.timedelta(0)

    def test_multiple_usage_sessions_accumulate(self):
        electrodomestico = Electrodomestico(
            nombre="lavadora",
            potencia=10,
            tiempo_uso=datetime.timedelta(minutes=10),
        )
        
        electrodomestico.iniciar_uso()
        electrodomestico.detener_uso()
        
        assert electrodomestico.tiempo_uso > datetime.timedelta(minutes=10)
