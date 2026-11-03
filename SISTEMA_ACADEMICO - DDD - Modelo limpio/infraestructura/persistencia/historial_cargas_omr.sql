CREATE TABLE IF NOT EXISTS historial_cargas_omr (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 carga_id BIGINT NOT NULL,
 accion ENUM('REINTENTO','REEMPLAZO') NOT NULL,
 usuario_id INT NOT NULL,
 motivo TEXT NOT NULL,
 datos_anteriores JSON NOT NULL,
 creada_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(carga_id) REFERENCES cargas_omr(id),
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id_usuario),
 INDEX idx_historial_carga(carga_id,id)
) ENGINE=InnoDB;
