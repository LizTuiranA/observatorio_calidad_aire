"""Servicio de notificación por correo electrónico."""

class EmailService:
    """Simula el envío de notificaciones por correo."""
    
    def enviar_notificacion(self, accion, detalles):
        # En un entorno real, aquí usarías smtplib o una API de correos.
        print(f"\n[📧 EMAIL SERVICE] Notificación enviada.")
        print(f"Asunto: Operación de {accion} en Municipio")
        print(f"Mensaje: {detalles}\n")