"""Tab de Alertas (dummy, pendiente de implementacion)."""

from tkinter import ttk


class AlertasTab:
    def __init__(self, parent: ttk.Frame) -> None:
        ttk.Label(
            parent,
            text="Pestana de Alertas (pendiente de implementacion)",
            padding=20,
        ).pack(expand=True)
