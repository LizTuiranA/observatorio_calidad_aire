class VisitanteController:
    """Coordinador para la lectura pública de mediciones y alertas."""
    def __init__(self, medicion_controller, alerta_controller):
        self.medicion_controller = medicion_controller
        self.alerta_controller = alerta_controller

    def obtener_mediciones(self, id_municipio_filtro=None):
        mediciones = self.medicion_controller.listar_mediciones()
        if id_municipio_filtro:
            return [m for m in mediciones if getattr(m, 'id_municipio', None) == id_municipio_filtro]
        return mediciones

    def obtener_alertas(self, id_municipio_filtro=None):
        alertas = self.alerta_controller.listar_alertas()
        if id_municipio_filtro:
            return [a for a in alertas if getattr(a, 'id_municipio', None) == id_municipio_filtro]
        return alertas