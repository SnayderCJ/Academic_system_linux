from abstracta import Alumno, Estudiante
from datetime import date

class Nota:
    def __init__(self, id, periodo, profesor, asignatura, active):
        self.id = id  # Identificador único para la nota.
        self.periodo = periodo  # Periodo en el que se otorga la nota.
        self.profesor = profesor  # Profesor que otorga la nota.
        self.asignatura = asignatura  # Asignatura a la que pertenece la nota.
        self.detalleNota = []  # Lista para almacenar los detalles de las notas para cada estudiante.
        self.fecha_creacion = date.today()  # Fecha de creación del registro de la nota, se asigna la fecha actual.
        self.active = active  # Estado de actividad de la nota (True o False).
        
    def addNota(self):
        pass  # Método placeholder para añadir detalles de la nota.