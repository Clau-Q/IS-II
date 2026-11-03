"""Permite ejecutar python -m addison_omr."""

# ACCESO CLI — python -m addison_omr (paso 1.1).
from .recibir_argumentos_cli import main

if __name__ == "__main__":
    raise SystemExit(main())
