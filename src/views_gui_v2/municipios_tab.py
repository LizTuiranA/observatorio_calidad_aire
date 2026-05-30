"""Tab de Municipios (dummy, pendiente de implementacion)."""

from tkinter import ttk


class MunicipiosTab:
	def __init__(self, parent: ttk.Frame) -> None:
		ttk.Label(
			parent,
			text="Pestana de Municipios (pendiente de implementacion)",
			padding=20,
		).pack(expand=True)

