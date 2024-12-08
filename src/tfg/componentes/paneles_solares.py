from pydantic import BaseModel


class PanelSolar(BaseModel):
    tamaño: float
    eficiencia: float

    def calcular_generacion_serie(self, serie_irradiacion: list[float]) -> float:
        """
        Calcula la energía generada total (W) mediante una serie de irradiacion por hora.
        """
        return sum(
            self.calcular_generacion_estimada_hora(irradiacion)
            for irradiacion in serie_irradiacion
        )

    def calcular_generacion_estimada_hora(self, irradiacion: float) -> float:
        """
        Calcula la energía generada por hora.

        Usa la fórmula irradiación(W/m^2) * tamaño(m^2) * eficiencia (%) y se se estima una hora de uso.
        """
        return self.tamaño * irradiacion * self.eficiencia
