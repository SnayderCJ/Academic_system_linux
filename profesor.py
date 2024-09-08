from datetime import date

# Clase que representa un profesor.
class Profesor:
    def __init__(self, id, nombre, active):
        self.id = id  # Identificador único para el profesor.
        self.nombre = nombre  # Nombre del profesor.
        self.fecha_creacion = date.today()  # Fecha de creación del registro del profesor, se asigna la fecha actual.
        self.active = active  # Estado de actividad del profesor (True o False).

    @property
    def id(self):
        """Obtiene el identificador único del profesor."""
        return self._id

    @property
    def nombre(self):
        """Obtiene el nombre del profesor."""
        return self._nombre
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del profesor."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtiene el estado de actividad del profesor."""
        return self._active