"""Servicio de notificación por correo electrónico."""

class EmailService:
    """Simula el envío de notificaciones por correo."""
    
    def enviar_notificacion(self, accion, detalles):
        print(f"\n[📧 EMAIL SERVICE] Notificación enviada.")
        print(f"Asunto: Operación de {accion} en Municipio")
        print(f"Mensaje: {detalles}\n")