import datetime

from tfg.componentes.bateria import Bateria


class TestBaterias:
    def test_calculate_percentage(self):
        bateria = Bateria(carga_max=50, carga_actual=20)
        assert bateria.porcentaje == 0.4

    def test_battery_states(self):
        bateria_vacia = Bateria(carga_max=100, carga_actual=0)
        assert bateria_vacia.esta_descargada
        assert not bateria_vacia.esta_cargada

        bateria_llena = Bateria(carga_max=100, carga_actual=100)
        assert bateria_llena.esta_cargada
        assert not bateria_llena.esta_descargada

        bateria_parcial = Bateria(carga_max=100, carga_actual=50)
        assert not bateria_parcial.esta_cargada
        assert not bateria_parcial.esta_descargada

    def test_tiempo_carga_descarga(self):
        bateria = Bateria(carga_max=100, carga_actual=50)

        tiempo_carga = bateria.tiempo_hasta_carga_completa(25)  # 25W
        expected_hours = (100 - 50) / 25  # 2 hours
        assert tiempo_carga == datetime.timedelta(hours=expected_hours)

        tiempo_descarga = bateria.tiempo_hasta_descarga_completa(10)  # 10W
        expected_hours = 50 / 10  # 5 hours
        assert tiempo_descarga == datetime.timedelta(hours=expected_hours)

    def test_capacidad_carga_disponible(self):
        bateria = Bateria(carga_max=100, carga_actual=30)
        assert bateria.capacidad_carga_disponible() == 70

    def test_puede_proporcionar_potencia(self):
        bateria_con_carga = Bateria(carga_max=100, carga_actual=50)
        bateria_sin_carga = Bateria(carga_max=100, carga_actual=0)

        assert bateria_con_carga.puede_proporcionar_potencia(10)
        assert not bateria_sin_carga.puede_proporcionar_potencia(10)
