"""Dialogos de acceso para la GUI Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.cli.auth import AuthService
from src.services.session_context import SesionActiva


class RoleSelector:
    """Ventana de bienvenida para seleccionar el rol antes de entrar."""

    def __init__(self, parent: tk.Tk | None = None, auth_service: AuthService | None = None) -> None:
        self.parent = parent
        self.auth_service = auth_service or AuthService()
        self._sesion: SesionActiva | None = None
        self._window: tk.Toplevel | None = None

    def seleccionar(self) -> SesionActiva | None:
        if self.parent is None:
            self._window = tk.Tk()
        else:
            self._window = tk.Toplevel(self.parent)
        self._window.title("Observatorio de Calidad del Aire")
        self._window.resizable(False, False)
        self._window.configure(padx=24, pady=22)
        if self.parent is not None:
            self._window.transient(self.parent)
        self._window.grab_set()
        self._window.protocol("WM_DELETE_WINDOW", self._cerrar)
        self._window.deiconify()
        self._window.lift()
        self._window.attributes("-topmost", True)

        self._centrar(620, 360)

        contenedor = ttk.Frame(self._window, padding=16)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Observatorio de Calidad del Aire",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="center", pady=(4, 8))

        ttk.Label(
            contenedor,
            text=(
                "Seleccione su tipo de acceso para continuar.\n"
                "Visitante entra en modo consulta; Empleado requiere autenticaci\u00f3n."
            ),
            justify="center",
        ).pack(anchor="center", pady=(0, 20))

        botones = ttk.Frame(contenedor)
        botones.pack(fill="x", pady=(6, 8))
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)

        ttk.Button(
            botones,
            text="Empleado",
            command=self._abrir_login,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8), ipady=10)

        ttk.Button(
            botones,
            text="Visitante",
            command=self._seleccionar_visitante,
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0), ipady=10)

        ttk.Label(
            contenedor,
            text="Acceso centrado en roles, sin selecci\u00f3n por texto.",
            foreground="#6b7280",
        ).pack(anchor="center", pady=(12, 0))

        self._window.after(100, lambda: self._window and self._window.attributes("-topmost", False))
        self._window.after(0, self._window.focus_force)

        if self.parent is None:
            self._window.mainloop()
        else:
            self._window.wait_window()
        return self._sesion

    def _abrir_login(self) -> None:
        login = EmployeeLoginDialog(self._window, self.auth_service)
        if login.ejecutar():
            self._sesion = login.obtener_sesion()
            self._cerrar()

    def _seleccionar_visitante(self) -> None:
        self._sesion = SesionActiva(usuario="visitante", rol="visitante")
        self._cerrar()

    def _cerrar(self) -> None:
        if self._window is not None:
            self._window.destroy()
            self._window = None

    def _centrar(self, ancho: int, alto: int) -> None:
        host = self._window or self.parent
        if host is None:
            return
        host.update_idletasks()
        x = (host.winfo_screenwidth() - ancho) // 2
        y = (host.winfo_screenheight() - alto) // 2
        self._window.geometry(f"{ancho}x{alto}+{x}+{y}")


class EmployeeLoginDialog:
    """Ventana modal de login para empleados."""

    def __init__(self, parent: tk.Toplevel | tk.Tk, auth_service: AuthService) -> None:
        self.parent = parent
        self.auth_service = auth_service
        self._window: tk.Toplevel | None = None
        self._usuario = tk.StringVar()
        self._clave = tk.StringVar()
        self._mensaje = tk.StringVar(value="Ingresa tus credenciales para continuar.")
        self._aceptado = False
        self._usuario_autenticado = ""
        self._intentos = 0
        self._bloqueado = False
        self._entrada_usuario: ttk.Entry | None = None
        self._entrada_clave: ttk.Entry | None = None
        self._btn_ingresar: ttk.Button | None = None

    def ejecutar(self) -> bool:
        self._window = tk.Toplevel(self.parent)
        self._window.title("Acceso de empleado")
        self._window.resizable(False, False)
        self._window.configure(padx=24, pady=20)
        self._window.transient(self.parent)
        self._window.grab_set()
        self._window.protocol("WM_DELETE_WINDOW", self._volver)

        self._centrar(520, 300)

        contenedor = ttk.Frame(self._window, padding=16)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Acceso de empleado",
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(contenedor, textvariable=self._mensaje, wraplength=420).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        ttk.Label(contenedor, text="Usuario").grid(row=2, column=0, sticky="w", pady=4)
        self._entrada_usuario = ttk.Entry(contenedor, textvariable=self._usuario, width=34)
        self._entrada_usuario.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(contenedor, text="Contraseña").grid(row=3, column=0, sticky="w", pady=4)
        self._entrada_clave = ttk.Entry(contenedor, textvariable=self._clave, width=34, show="*")
        self._entrada_clave.grid(row=3, column=1, sticky="ew", pady=4)

        botones = ttk.Frame(contenedor)
        botones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(18, 0))
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)

        ttk.Button(botones, text="Volver", command=self._volver).grid(
            row=0, column=0, sticky="ew", padx=(0, 8)
        )
        self._btn_ingresar = ttk.Button(botones, text="Ingresar", command=self._validar)
        self._btn_ingresar.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        self._window.bind("<Return>", lambda _event: self._validar())
        self._entrada_clave.focus_set()
        self._window.wait_window()
        return self._aceptado

    def _validar(self) -> None:
        if self._bloqueado:
            self._mensaje.set("Acceso bloqueado. Debes volver a la pantalla inicial.")
            return

        usuario = self._usuario.get().strip()
        clave = self._clave.get().strip()
        if self.auth_service.validar_credenciales(usuario, clave):
            self._aceptado = True
            self._usuario_autenticado = usuario
            self._mensaje.set("Acceso concedido.")
            self._cerrar()
            return

        self._intentos += 1
        intentos_restantes = self.auth_service.max_attempts - self._intentos
        if intentos_restantes <= 0:
            self._bloquear_acceso()
            return

        self._mensaje.set(
            f"Usuario o contraseña incorrectos. Intentos restantes: {intentos_restantes}."
        )
        self._clave.set("")
        if self._entrada_clave is not None:
            self._entrada_clave.focus_set()

    def _bloquear_acceso(self) -> None:
        self._bloqueado = True
        self._mensaje.set(
            "Acceso bloqueado tras 3 intentos fallidos. Vuelve a la pantalla inicial."
        )
        if self._entrada_usuario is not None:
            self._entrada_usuario.state(["disabled"])
        if self._entrada_clave is not None:
            self._entrada_clave.state(["disabled"])
        if self._btn_ingresar is not None:
            self._btn_ingresar.state(["disabled"])

    def _volver(self) -> None:
        self._aceptado = False
        self._cerrar()

    def _cerrar(self) -> None:
        if self._window is not None:
            self._window.destroy()
            self._window = None

    def obtener_sesion(self) -> SesionActiva | None:
        """Retorna la sesion creada tras un acceso valido."""
        if not self._aceptado:
            return None
        usuario = self._usuario_autenticado or self._usuario.get().strip() or "empleado"
        return SesionActiva(usuario=usuario, rol="empleado")

    def _centrar(self, ancho: int, alto: int) -> None:
        self.parent.update_idletasks()
        x = (self.parent.winfo_screenwidth() - ancho) // 2
        y = (self.parent.winfo_screenheight() - alto) // 2
        self._window.geometry(f"{ancho}x{alto}+{x}+{y}")
