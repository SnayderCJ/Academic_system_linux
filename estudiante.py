from datetime import date

class Estudiante:
    """Representa a un estudiante en el sistema académico."""

    def __init__(self, id, nombre, apellido, fecha_nacimiento, active=True):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self.fecha_creacion = date.today().strftime('%Y-%m-%d')
        self._active = active

    @property
    def id(self):
        """Obtiene el identificador único del estudiante."""
        return self._id

    @property
    def nombre(self):
        """Obtiene el nombre del estudiante."""
        return self._nombre

    @property
    def apellido(self):
        """Obtiene el apellido del estudiante."""
        return self._apellido

    @property
    def fecha_nacimiento(self):
        """Obtiene la fecha de nacimiento del estudiante."""
        return self._fecha_nacimiento
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del registro del estudiante."""
        return self._fecha_creacion

    @property
    def active(self):
        """Obtiene el estado de actividad del estudiante."""
        return self._active
    

    def calcular_edad(self):
        """Calcula la edad del estudiante a partir de su fecha de nacimiento."""
        hoy = date.today()
        edad = hoy.year - self._fecha_nacimiento.year - ((hoy.month, hoy.day) < (self._fecha_nacimiento.month, self._fecha_nacimiento.day))
        return edad