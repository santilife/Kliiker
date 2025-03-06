from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
    Response,
)

# Importacion de functools
import functools

# ----------------- Se crea el decorador para login_required ----------------- #


def login_required(route):
    @functools.wraps(route)
    def router_wrapper(*args, **kwargs):
        if not session.get("logueado"):  # Verifica si el usuario NO está logueado
            return redirect(url_for("iniciar_sesion.login"))
        return route(*args, **kwargs)

    return router_wrapper


# Se crea el decorador para restringir las paginas de Administrador y de Asesor
def role_required(role):
    def decorator(route):
        @functools.wraps(route)
        def wrapper(*args, **kwargs):
            if session.get("rol") != role:
                return redirect(
                    url_for("iniciar_sesion.login")
                )  # O en vez de redirijir a login muestre un error 403
            return route(*args, **kwargs)

        return wrapper

    return decorator
