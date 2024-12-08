from tfg.componentes.baterias import Bateria


class TestBaterias:
    def test_calculate_percentage(self):
        bateria = Bateria(carga_max=50, carga_actual=20)

        assert bateria.porcentaje == 0.4