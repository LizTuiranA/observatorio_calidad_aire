"""Punto de entrada único del proyecto."""

from dotenv import load_dotenv
import tkinter as tk

from src.views_gui_v2.app_window import AppWindow
from src.views_gui_v2.auth_dialogs import RoleSelector


load_dotenv()


def main() -> None:
    """Abre la pantalla de bienvenida y luego la GUI principal."""
    selector = RoleSelector()
    rol = selector.seleccionar()
    if rol is None:
        return

    app_root = tk.Tk()
    AppWindow(app_root, role=rol)
    app_root.mainloop()


if __name__ == "__main__":
    main()