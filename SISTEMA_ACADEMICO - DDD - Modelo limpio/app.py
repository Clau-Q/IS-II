import os
import secrets
from functools import wraps

import click
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from aplicacion.servicios.cuenta_usuario_app_service import CuentaUsuarioAppService
from infraestructura.persistencia.repositories.cuenta_usuario_orm_repositorio import CuentaUsuarioORMRepositorio
from infraestructura.seguridad.protector_credenciales_werkzeug import ProtectorCredencialesWerkzeug
from aplicacion.servicios.estudiante_app_service import EstudianteAppService
from infraestructura.persistencia.repositories.estudiante_orm_repositorio import EstudianteORMRepositorio
from sqlalchemy.exc import IntegrityError
from aplicacion.servicios.gestion_usuarios_app_service import GestionUsuariosAppService
from infraestructura.persistencia.repositories.gestion_usuarios_repositorio import GestionUsuariosRepositorio
from infraestructura.persistencia.repositories.organizacion_repositorio import OrganizacionRepositorio


def crear_app(servicio_prueba=None):
    app = Flask(__name__, template_folder="presentacion/plantillas", static_folder="presentacion/vistas/recursos", static_url_path="/recursos")
    app.secret_key = os.environ.get("SISTEMA_SECRET_KEY") or secrets.token_hex(32)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
    database_url = os.environ.get("SISTEMA_DATABASE_URL")
    engine = create_engine(database_url, pool_pre_ping=True) if database_url else None
    servicio = servicio_prueba or (CuentaUsuarioAppService(CuentaUsuarioORMRepositorio(engine), ProtectorCredencialesWerkzeug()) if engine else None)
    estudiantes_servicio = EstudianteAppService(EstudianteORMRepositorio(engine)) if engine else None
    usuarios_servicio = GestionUsuariosAppService(GestionUsuariosRepositorio(engine), ProtectorCredencialesWerkzeug()) if engine else None
    organizacion_repo = OrganizacionRepositorio(engine) if engine else None

    @app.cli.command("activar-coordinador")
    @click.password_option(prompt="Contraseña para el coordinador inicial", confirmation_prompt=True)
    def activar_coordinador(password):
        """Establece la contraseña y activa el coordinador inicial del SQL."""
        if not engine:
            raise click.ClickException("Configure SISTEMA_DATABASE_URL primero.")
        if len(password) < 8:
            raise click.ClickException("La contraseña debe tener al menos 8 caracteres.")
        try:
            with engine.begin() as conexion:
                resultado = conexion.execute(text("UPDATE usuarios SET password_hash = :clave, estado = 'ACTIVO' WHERE username = 'coordinador' AND estado = 'INACTIVO'"), {"clave": ProtectorCredencialesWerkzeug().generar_hash(password)})
                if resultado.rowcount != 1:
                    raise click.ClickException("No se encontró el coordinador inicial inactivo.")
        except SQLAlchemyError as error:
            raise click.ClickException("No se pudo actualizar la cuenta. Revise la conexión y el esquema.") from error
        click.echo("Cuenta coordinador activada.")

    def proteger(rol):
        def decorador(funcion):
            @wraps(funcion)
            def vista(*args, **kwargs):
                if not session.get("usuario"):
                    return redirect(url_for("login"))
                roles = session.get("roles", [])
                if rol not in roles and not (rol == "COORDINADOR" and "DIRECTOR" in roles):
                    abort(403)
                return funcion(*args, **kwargs)
            return vista
        return decorador

    @app.before_request
    def csrf():
        if request.method == "POST":
            token = session.get("csrf_token", "")
            if not token or not secrets.compare_digest(token, request.form.get("csrf_token", "")):
                abort(400)

    @app.context_processor
    def token_csrf():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        return {"csrf_token": session["csrf_token"]}

    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if servicio is None:
                flash("Configure la conexión a la base de datos para iniciar sesión.", "error")
                return render_template("login.html"), 503
            try:
                cuenta = servicio.iniciar_sesion(request.form.get("usuario", ""), request.form.get("contrasena", ""))
            except SQLAlchemyError:
                app.logger.exception("Error de conexión al consultar la cuenta")
                flash("No se pudo consultar la base de datos. Revise la conexión.", "error")
                return render_template("login.html"), 503
            if not cuenta:
                flash("Usuario o contraseña incorrectos, o cuenta inactiva.", "error")
                return render_template("login.html"), 401
            roles = [rol for rol in cuenta["roles"] if rol in ("COORDINADOR", "DIRECTOR")]
            if not roles:
                flash("Esta cuenta no tiene acceso a los paneles disponibles.", "error")
                return render_template("login.html"), 403
            session.clear()
            session.update(usuario=cuenta["usuario"], nombre=cuenta["nombre"], roles=roles)
            return redirect(url_for("elegir_rol") if len(roles) > 1 else url_for(roles[0].lower()))
        return render_template("login.html")

    @app.get("/elegir-rol")
    def elegir_rol():
        if not session.get("usuario"):
            return redirect(url_for("login"))
        return render_template("elegir_rol.html", roles=session["roles"])

    @app.get("/coordinador")
    @proteger("COORDINADOR")
    def coordinador():
        pendientes = None
        if engine:
            try:
                with engine.connect() as conexion:
                    pendientes = conexion.execute(text("SELECT (SELECT COUNT(*) FROM preguntas WHERE estado='REVISION') AS preguntas, (SELECT COUNT(*) FROM respuestas_detectadas WHERE requiere_revision=1) AS lecturas, (SELECT COUNT(*) FROM resultados_examen WHERE estado='CALCULADO' AND vigente=1) AS calculos, (SELECT COUNT(*) FROM resultados_examen WHERE estado='REVISADO' AND vigente=1) AS publicaciones")).mappings().one()
            except SQLAlchemyError:
                app.logger.exception("No se pudieron consultar los pendientes")
        return render_template("inicio.html", rol="Coordinador", nombre=session["nombre"], pendientes=pendientes)

    @app.route("/coordinador/estudiantes", methods=["GET", "POST"])
    @proteger("COORDINADOR")
    def estudiantes():
        if not estudiantes_servicio:
            abort(503)
        if request.method == "POST":
            try:
                estudiantes_servicio.registrar_estudiante(request.form)
                flash("Estudiante registrado correctamente.", "ok")
                return redirect(url_for("estudiantes"))
            except ValueError as error:
                flash(str(error), "error")
            except IntegrityError:
                flash("El código del estudiante ya está registrado.", "error")
        try:
            lista = estudiantes_servicio.listar(request.args.get("q", ""))
        except SQLAlchemyError:
            app.logger.exception("Error al consultar estudiantes")
            abort(503)
        return render_template("estudiantes.html", rol="Coordinador", nombre=session["nombre"], estudiantes=lista, busqueda=request.args.get("q", ""))

    @app.route("/coordinador/estudiantes/<int:id>/editar", methods=["GET", "POST"])
    @proteger("COORDINADOR")
    def editar_estudiante(id):
        if not estudiantes_servicio:
            abort(503)
        registro = estudiantes_servicio.repositorio.buscar_por_id(id)
        if not registro:
            abort(404)
        if request.method == "POST":
            try:
                estudiantes_servicio.actualizar(id, request.form)
                flash("Estudiante actualizado correctamente.", "ok")
                return redirect(url_for("estudiantes"))
            except ValueError as error:
                flash(str(error), "error")
            except IntegrityError:
                flash("El código del estudiante ya está registrado.", "error")
        return render_template("editar_estudiante.html", rol="Coordinador", nombre=session["nombre"], estudiante=registro)

    @app.post("/coordinador/estudiantes/<int:id>/estado")
    @proteger("COORDINADOR")
    def estado_estudiante(id):
        try:
            if not estudiantes_servicio.cambiar_estado(id, request.form.get("estado", "")):
                abort(404)
            flash("Estado actualizado.", "ok")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("estudiantes"))

    @app.post("/coordinador/estudiantes/<int:id>/cuenta")
    @proteger("COORDINADOR")
    def vincular_estudiante(id):
        try:
            estudiantes_servicio.vincular_cuenta(id, request.form.get("usuario", ""))
            flash("Cuenta vinculada correctamente.", "ok")
        except ValueError as error:
            flash(str(error), "error")
        except IntegrityError:
            flash("Esa cuenta ya está vinculada a otro estudiante.", "error")
        return redirect(url_for("editar_estudiante", id=id))

    @app.get("/director")
    @proteger("DIRECTOR")
    def director():
        return render_template("inicio.html", rol="Director", nombre=session["nombre"])

    @app.route("/coordinador/usuarios", methods=["GET", "POST"])
    @proteger("COORDINADOR")
    def usuarios():
        if not usuarios_servicio:
            abort(503)
        director_activo = "DIRECTOR" in session["roles"]
        if request.method == "POST":
            try:
                usuarios_servicio.crear(request.form, director_activo)
                flash("Cuenta creada correctamente.", "ok")
                return redirect(url_for("usuarios"))
            except (ValueError, PermissionError) as error:
                flash(str(error), "error")
            except IntegrityError:
                flash("El nombre de usuario ya está registrado.", "error")
        try:
            lista = usuarios_servicio.repositorio.listar()
        except SQLAlchemyError:
            app.logger.exception("Error al consultar usuarios")
            abort(503)
        return render_template("usuarios.html", rol="Coordinador", nombre=session["nombre"], usuarios=lista, es_director=director_activo)

    @app.post("/coordinador/usuarios/<int:id>/estado")
    @proteger("COORDINADOR")
    def estado_usuario(id):
        if not usuarios_servicio:
            abort(503)
        try:
            usuarios_servicio.cambiar_estado(id, request.form.get("estado", ""), "DIRECTOR" in session["roles"])
            flash("Estado actualizado.", "ok")
        except (ValueError, PermissionError) as error:
            flash(str(error), "error")
        return redirect(url_for("usuarios"))

    @app.route("/coordinador/organizacion", methods=["GET", "POST"])
    @proteger("COORDINADOR")
    def organizacion():
        if not organizacion_repo:
            abort(503)
        if request.method == "POST":
            try:
                accion = request.form.get("accion")
                tipo = request.form.get("tipo", "")
                if accion == "asignar":
                    organizacion_repo.asignar(int(request.form.get("docente", "0")), int(request.form.get("materia", "0")))
                elif tipo not in OrganizacionRepositorio.CONSULTAS:
                    raise ValueError("Tipo de elemento no válido.")
                elif accion == "crear":
                    nombre = request.form.get("nombre", "").strip()
                    if not nombre:
                        raise ValueError("El nombre es obligatorio.")
                    datos = {"nombre": nombre, "codigo": request.form.get("codigo", "").strip(), "id_eje": int(request.form.get("id_eje") or 0), "id_ciclo": int(request.form.get("id_ciclo") or 0)}
                    if tipo == "areas" and not datos["codigo"]:
                        raise ValueError("El código del área es obligatorio.")
                    organizacion_repo.crear(tipo, datos)
                elif accion == "estado":
                    estado = request.form.get("estado")
                    if estado not in ("ACTIVO", "INACTIVO"):
                        raise ValueError("Estado no válido.")
                    if not organizacion_repo.estado(tipo, int(request.form.get("id", "0")), estado):
                        raise ValueError("Elemento no encontrado o sin cambios.")
                else:
                    raise ValueError("Acción no válida.")
                flash("Operación realizada correctamente.", "ok")
                return redirect(url_for("organizacion"))
            except ValueError as error:
                flash(str(error), "error")
            except IntegrityError:
                flash("No se pudo guardar: comprueba el código o el elemento seleccionado.", "error")
        return render_template("organizacion.html", rol="Coordinador", nombre=session["nombre"], catalogos=organizacion_repo.listar())

    @app.post("/salir")
    def salir():
        session.clear()
        return redirect(url_for("login"))

    return app


if __name__ == "__main__":
    crear_app().run(debug=False)
