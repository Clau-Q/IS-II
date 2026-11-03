-- Los exámenes existentes se dejan cerrados para recibir preguntas.
ALTER TABLE examenes ADD COLUMN admite_preguntas BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE examenes ALTER COLUMN admite_preguntas SET DEFAULT TRUE;
