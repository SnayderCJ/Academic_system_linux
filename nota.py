from datetime import date
from detalleNota import DetalleNota

class Nota:
    """Representa una nota asociada a un periodo, profesor y asignatura."""

    def __init__(self, id, periodo, profesor, asignatura, active=True):
        self._id = id
        self._periodo = periodo
        self._profesor = profesor
        self._asignatura = asignatura
        self._detalleNota = []
        self._fecha_creacion = date.today()
        self._active = active

    # ... (Propiedades para los atributos)

    def add_detalle_nota(self, detalle_nota: DetalleNota):
        """Agrega un detalle de nota a la lista.

        Args:
            detalle_nota: La instancia de DetalleNota a agregar.

        Raises:
            ValueError: Si el estudiante ya tiene una nota registrada para esta asignatura y periodo.
        """
        estudiante_id = detalle_nota.estudiante.id
        if any(dn.estudiante.id == estudiante_id for dn in self._detalleNota):
            raise ValueError("El estudiante ya tiene una nota registrada para esta asignatura y periodo.")
        self._detalleNota.append(detalle_nota)

    # ... (Otros métodos según sea necesario)