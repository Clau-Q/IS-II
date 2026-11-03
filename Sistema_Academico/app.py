"""Composición de la aplicación Flask y sus dependencias."""
import os
import secrets
from pathlib import Path

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine

from aplicacion.servicios.cuenta_usuario_app_service import CuentaUsuarioAppService
from aplicacion.servicios.estudiante_app_service import EstudianteAppService
from aplicacion.servicios.gestion_usuarios_app_service import GestionUsuariosAppService
from aplicacion.servicios.organizacion_app_service import OrganizacionAppService
from aplicacion.servicios.panel_pendientes_app_service import PanelPendientesAppService
from infraestructura.persistencia.repositories.cuenta_usuario_orm_repositorio import CuentaUsuarioORMRepositorio
from infraestructura.persistencia.repositories.estudiante_orm_repositorio import EstudianteORMRepositorio
from infraestructura.persistencia.repositories.gestion_usuarios_repositorio import GestionUsuariosRepositorio
from infraestructura.persistencia.repositories.organizacion_repositorio import OrganizacionRepositorio
from infraestructura.persistencia.repositories.panel_pendientes_repositorio import PanelPendientesRepositorio
from infraestructura.seguridad.protector_credenciales_werkzeug import ProtectorCredencialesWerkzeug
from presentacion.controllers.rutas_web import registrar_rutas
from infraestructura.persistencia.repositories.evaluaciones_coordinador_repositorio import EvaluacionesCoordinadorRepositorio
from aplicacion.servicios.simulacro_app_service import SimulacroAppService
from aplicacion.servicios.pregunta_app_service import PreguntaAppService
from aplicacion.servicios.importacion_cartillas_app_service import ImportacionCartillasAppService
from infraestructura.persistencia.repositories.cargas_omr_repositorio import CargasOMRRepositorio
from infraestructura.archivos.preparador_cartillas import PreparadorCartillas
from infraestructura.vision.lector_burbujas_opencv import LectorBurbujasOpenCV


from aplicacion.servicios.calculo_resultado_app_service import CalculoResultadoAppService
from infraestructura.persistencia.repositories.calculo_resultados_repositorio import CalculoResultadosRepositorio
from aplicacion.servicios.diseno_examen_app_service import DisenoExamenAppService
from infraestructura.persistencia.repositories.diseno_examen_repositorio import DisenoExamenRepositorio
from aplicacion.servicios.docente_app_service import DocenteAppService
from infraestructura.persistencia.repositories.docente_repositorio import DocenteRepositorio
from infraestructura.archivos.imagenes_preguntas import ImagenesPreguntas
from aplicacion.servicios.resultados_app_service import ResultadosAppService
from infraestructura.persistencia.repositories.resultados_repositorio import ResultadosRepositorio


def crear_app(servicio_prueba=None):
    app = Flask(__name__, template_folder='presentacion/vistas', static_folder='presentacion/vistas/recursos', static_url_path='/recursos')
    app.secret_key = os.environ.get('SISTEMA_SECRET_KEY') or secrets.token_hex(32)
    CSRFProtect(app)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
    app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024
    database_url = os.environ.get('SISTEMA_DATABASE_URL')
    motor = create_engine(database_url, pool_pre_ping=True) if database_url else None
    protector = ProtectorCredencialesWerkzeug()
    acceso = servicio_prueba or (CuentaUsuarioAppService(CuentaUsuarioORMRepositorio(motor), protector) if motor else None)
    estudiantes = EstudianteAppService(EstudianteORMRepositorio(motor)) if motor else None
    usuarios = GestionUsuariosAppService(GestionUsuariosRepositorio(motor), protector) if motor else None
    organizacion = OrganizacionAppService(OrganizacionRepositorio(motor)) if motor else None
    panel = PanelPendientesAppService(PanelPendientesRepositorio(motor)) if motor else None
    evaluaciones = EvaluacionesCoordinadorRepositorio(motor) if motor else None
    simulacros = SimulacroAppService(evaluaciones) if motor else None
    preguntas = PreguntaAppService(evaluaciones) if motor else None
    cartillas = ImportacionCartillasAppService(CargasOMRRepositorio(motor), PreparadorCartillas(Path(__file__).parent / 'datos_privados' / 'cartillas'), LectorBurbujasOpenCV()) if motor else None
    resultados = ResultadosAppService(ResultadosRepositorio(motor)) if motor else None
    docente = DocenteAppService(DocenteRepositorio(motor)) if motor else None
    imagenes_preguntas = ImagenesPreguntas(Path(__file__).parent / 'datos_privados' / 'preguntas') if motor else None
    diseno = DisenoExamenAppService(DisenoExamenRepositorio(motor)) if motor else None
    calculo = CalculoResultadoAppService(CalculoResultadosRepositorio(motor)) if motor else None
    registrar_rutas(app, acceso, estudiantes, usuarios, organizacion, panel, simulacros, preguntas, cartillas, resultados, docente, imagenes_preguntas, diseno, calculo)
    return app


if __name__ == '__main__':
    crear_app().run(debug=False)
