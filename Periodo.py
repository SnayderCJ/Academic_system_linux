from datetime import date  # Importa la clase date del módulo datetime para manejar fechas.

class Periodo:
    def __init__(self, id, periodo, active):
        self.id = id  # Identificador único para el periodo.
        self.periodo = periodo  # Nombre o descripción del periodo (por ejemplo, "Semestre 1").
        self.fecha_creacion = date.today()  # Fecha de creación del periodo, se asigna la fecha actual.
        self.active = active  # Estado de actividad del periodo (True o False).