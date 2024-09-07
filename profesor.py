from datetime import date

# Clase que representa un profesor.
class Profesor:
    def __init__(self, id, nombre, active):
        self.id = id  # Identificador único para el profesor.
        self.nombre = nombre  # Nombre del profesor.
        self.fecha_creacion = date.today()  # Fecha de creación del registro del profesor, se asigna la fecha actual.
        self.active = active  # Estado de actividad del profesor (True o False).