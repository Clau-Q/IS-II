-- Aplicar una vez a instalaciones anteriores; conserva preguntas existentes.
ALTER TABLE preguntas ADD COLUMN id_examen_destino INT NULL;
CREATE INDEX idx_pregunta_examen_destino ON preguntas(id_examen_destino);
