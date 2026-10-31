from sqlalchemy import text


class OrganizacionRepositorio:
    CONSULTAS = {
        "areas": ("areas", "id_area", "codigo,nombre", "'ACTIVO','INACTIVO'"),
        "ejes": ("ejes_tematicos", "id_eje", "nombre", "'ACTIVO','INACTIVO'"),
        "materias": ("materias", "id_materia", "nombre,id_eje", "'ACTIVO','INACTIVO'"),
        "ciclos": ("ciclos_preparacion", "id_ciclo", "nombre", "'ACTIVO','INACTIVO'"),
        "grupos": ("grupos_academicos", "id_grupo", "nombre,id_ciclo", "'ACTIVO','INACTIVO'"),
    }

    def __init__(self, motor):
        self.motor = motor

    def listar(self):
        with self.motor.connect() as c:
            salida = {clave: c.execute(text(f"SELECT {id_columna} AS id, nombre, estado FROM {tabla} ORDER BY nombre")).mappings().all() for clave, (tabla, id_columna, _, _) in self.CONSULTAS.items()}
            salida["docentes"] = c.execute(text("SELECT d.id_docente AS id, CONCAT(u.nombres,' ',u.apellidos) AS nombre FROM docentes d JOIN usuarios u ON u.id_usuario=d.id_usuario WHERE u.estado='ACTIVO' ORDER BY nombre")).mappings().all()
            return salida

    def crear(self, tipo, datos):
        tabla, _, columnas, _ = self.CONSULTAS[tipo]
        nombres = columnas.split(",")
        parametros = {nombre: datos[nombre] for nombre in nombres}
        with self.motor.begin() as c:
            c.execute(text(f"INSERT INTO {tabla} ({columnas}) VALUES ({','.join(':'+n for n in nombres)})"), parametros)

    def estado(self, tipo, id, estado):
        tabla, id_columna, _, _ = self.CONSULTAS[tipo]
        with self.motor.begin() as c:
            return c.execute(text(f"UPDATE {tabla} SET estado=:estado WHERE {id_columna}=:id"), {"estado": estado, "id": id}).rowcount

    def asignar(self, docente, materia):
        with self.motor.begin() as c:
            docente_valido = c.execute(text("SELECT d.id_docente FROM docentes d JOIN usuarios u ON u.id_usuario=d.id_usuario WHERE d.id_docente=:id AND u.estado='ACTIVO' FOR UPDATE"), {"id": docente}).scalar_one_or_none()
            materia_valida = c.execute(text("SELECT id_materia FROM materias WHERE id_materia=:id AND estado='ACTIVO' FOR UPDATE"), {"id": materia}).scalar_one_or_none()
            if not docente_valido or not materia_valida:
                raise ValueError("Selecciona un docente y una materia activos.")
            c.execute(text("INSERT INTO docente_materias(id_docente,id_materia,fecha_asignacion,estado) VALUES (:docente,:materia,CURRENT_DATE,'ACTIVO') ON DUPLICATE KEY UPDATE estado='ACTIVO', fecha_asignacion=CURRENT_DATE"), {"docente": docente, "materia": materia})
