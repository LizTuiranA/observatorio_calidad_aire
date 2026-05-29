"""Tab de Estaciones (dummy, pendiente de implementacion)."""

from tkinter import ttk


class EstacionesTab:
    def __init__(self, parent: ttk.Frame) -> None:
        ttk.Label(
            parent,
            text="Pestana de Estaciones (pendiente de implementacion)",
            padding=20,
        ).pack(expand=True)
