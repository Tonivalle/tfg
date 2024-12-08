from tfg.componentes.paneles_solares import PanelSolar


class TestPanelesSolares:
    def test_calculate_predicted_generation(self):
        panel = PanelSolar(tamaño=5, eficiencia=0.75)

        assert panel.calcular_generacion_estimada_hora(2381) == 8928.75

    def test_calculate_generation(self):
        panel = PanelSolar(tamaño=5, eficiencia=0.75)

        assert (
            panel.calcular_generacion_serie([43, 188, 318, 394, 435, 410, 330, 205, 58])
            == 8928.75
        )
