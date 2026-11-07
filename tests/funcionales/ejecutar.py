"""Ejecuta las pruebas funcionales y guarda el reporte de unittest."""
import io
from pathlib import Path
import sys
import unittest

CARPETA = Path(__file__).resolve().parent
sys.path.insert(0, str(CARPETA))


def main():
    try:
        import selenium
    except ImportError:
        print("Instala las dependencias de tests/funcionales/requirements.txt.")
        return 2
    reportes = CARPETA / "reportes"
    reportes.mkdir(exist_ok=True)
    suite = unittest.defaultTestLoader.discover(str(CARPETA), pattern="test_*.py")
    memoria = io.StringIO()
    resultado = unittest.TextTestRunner(stream=memoria, verbosity=2).run(suite)
    contenido = memoria.getvalue()
    (reportes / "ejecucion.txt").write_text(contenido, encoding="utf-8")
    print(contenido)
    print("Reporte: " + str(reportes / "ejecucion.txt"))
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
