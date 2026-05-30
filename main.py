"""Punto de entrada único del proyecto."""

from dotenv import load_dotenv
import tkinter as tk

from src.views_gui_v2.app_window import AppWindow
from src.views_gui_v2.auth_dialogs import RoleSelector


load_dotenv()


def main() -> None:
    """Abre la pantalla de bienvenida y luego la GUI principal."""
    selector = RoleSelector()
    sesion = selector.seleccionar()
    if sesion is None:
        return

    app_root = tk.Tk()
    AppWindow(app_root, session=sesion)
    app_root.mainloop()


if __name__ == "__main__":
    main()