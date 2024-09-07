from datetime import date  # Importa la clase date del módulo datetime para manejar fechas.

# Clase que representa una asignatura o materia dentro de un nivel educativo.
class Asignatura:
    def __init__(self, id, descripcion, nivel, active):
        self.id = id  # Identificador único para la asignatura.
        self.descripcion = descripcion  # Nombre o descripción de la asignatura (por ejemplo, "Matemáticas").
        self.nivel = nivel  # Nivel educativo al que pertenece la asignatura.
        self.fecha_creacion = date.today()  # Fecha de creación de la asignatura, se asigna la fecha actual.
        self.active = active  # Estado de actividad de la asignatura (True o False).