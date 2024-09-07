# Clase que representa los detalles de una nota para un estudiante específico.
class DetalleNota:
    def __init__(self, id, estudiante, nota1, nota2, recuperacion=None, observacion=None):
        self.id = id  # Identificador único para el detalle de la nota.
        self.estudiante = estudiante  # Estudiante al que se le asigna la nota.
        self.nota1 = nota1  # Primera calificación parcial.
        self.nota2 = nota2  # Segunda calificación parcial.
        self.recuperacion = recuperacion  # Nota de recuperación, opcional.
        self.observacion = observacion  # Observaciones sobre el rendimiento del estudiante, opcional.