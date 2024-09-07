from datetime import date

# Clase que representa un nivel educativo (por ejemplo, primaria, secundaria).
class Nivel:
    def __init__(self, id, nivel):
        self.id = id  # Identificador único para el nivel.
        self.nivel = nivel  # Nombre o descripción del nivel (por ejemplo, "Secundaria").
        self.fecha_creacion = date.today()  # Fecha de creación del nivel, se asigna la fecha actual.
        self.active = True  # El nivel se marca como activo de manera predeterminada.