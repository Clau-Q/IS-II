"""Ejecutar desde cualquier carpeta con el Python del entorno del proyecto."""
import os
from pathlib import Path
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = Path(__file__).resolve().parent
REPORTES = CARPETA / "reportes"
CONFIGURACION = str(CARPETA / ".coveragerc")


def ejecutar(argumentos, salida=None):
    resultado = subprocess.run(
        [sys.executable, "-B", "-m", "coverage", *argumentos],
        cwd=RAIZ,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    contenido = resultado.stdout + resultado.stderr
    if salida is not None:
        salida.write_text(contenido, encoding="utf-8")
    print(contenido, end="")
    return resultado.returncode


def main():
    REPORTES.mkdir(parents=True, exist_ok=True)
    codigo = ejecutar([
        "run", "--rcfile=" + CONFIGURACION, "-m", "unittest", "discover",
        "-s", str(CARPETA), "-p", "test_*.py", "-v"
    ], REPORTES / "ejecucion.txt")
    if codigo:
        return codigo
    codigo = ejecutar([
        "report", "--rcfile=" + CONFIGURACION
    ], REPORTES / "cobertura.txt")
    if codigo:
        return codigo
    return ejecutar([
        "html", "--rcfile=" + CONFIGURACION
    ])


if __name__ == "__main__":
    sys.exit(main())
