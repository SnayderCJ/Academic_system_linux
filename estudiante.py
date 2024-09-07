from datetime import date

# Clase que representa un estudiante.
class Estudiante:
    def __init__(self, id, nombre, active):
        self.id = id  # Identificador único para el estudiante.
        self.nombre = nombre  # Nombre del estudiante.
        self.fecha_creacion = date.today()  # Fecha de creación del registro del estudiante, se asigna la fecha actual.
        self.active = active  # Estado de actividad del estudiante (True o False).