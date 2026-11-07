# Ciclo TDD: estado de CuentaUsuario

## Comportamiento esperado

- activar(): una cuenta con activa=False queda con activa=True.
- desactivar(): una cuenta con activa=True queda con activa=False.

Los casos están en test_cuenta_usuario.py. Ambos preparan una cuenta, ejecutan
un método y comprueban el estado con assertTrue o assertFalse.

## 1. Rojo: pruebas antes de implementar

Se creó el archivo de pruebas mientras activar() y desactivar() todavía
contenían pass. La ejecución produjo dos fallos de aserción:

- test_activar_cuenta: False is not true.
- test_desactivar_cuenta: True is not false.

Evidencia original: rojo.txt.
No se rompió código implementado para provocar el fallo.

## 2. Verde: implementación mínima

Después de observar los fallos, se sustituyeron únicamente esos dos pass:

```python
def activar(self):
    self.activa = True

def desactivar(self):
    self.activa = False
```

Se ejecutaron las mismas dos pruebas, sin cambiar sus expectativas. Ambas
pasaron. Evidencia: verde.txt.

## 3. Revisión de refactorización

Se revisaron los nombres, la claridad y la duplicación. Cada método tiene una
sola asignación y las pruebas mantienen datos explícitos. No se identificó una
refactorización necesaria; no se añadieron abstracciones artificiales.

La ejecución final del conjunto y su cobertura se guardan en
../ejecucion.txt y ../cobertura.txt.

## Reproducir las pruebas del estado final

Desde la raíz del proyecto:

```powershell
.\.venv-1\Scripts\python.exe -B -m unittest discover -s tests\identidad_acceso -p "test_cuenta_usuario.py" -v
```

Ahora el comando debe pasar, porque los métodos ya están implementados.
El reporte rojo conserva la evidencia de la ejecución previa; este comando
no intenta recrearla modificando el código actual.

Este ciclo corresponde a las dos funciones nuevas; no demuestra TDD para
las otras pruebas de comportamiento previamente existente.
