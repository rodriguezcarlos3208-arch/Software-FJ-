from src.entidad import EntidadSistema
from src.cliente import Cliente
from src.servicios import Servicio
from src.excepciones import ServicioNoDisponibleError, OperacionNoPermitidaError

class Reserva(EntidadSistema):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int):
        super().__init__(id_reserva)
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    def confirmar(self, descuento: float = 0.0, recargo: float = 0.0):
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"La reserva {self._id} no se puede confirmar en estado {self._estado}.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible actualmente.")

        self._costo_total = self._servicio.calcular_costo_total(
            horas=self._horas,
            descuento=descuento,
            recargo=recargo
        )
        self._servicio.disponible = False
        self._estado = "CONFIRMADA"

    def cancelar(self):
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self._id} ya se encuentra cancelada.")
        if self._estado == "CONFIRMADA":
            self._servicio.disponible = True
        self._estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        return (f"Reserva [{self._id}] Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} ({self._horas}h) | "
                f"Estado: {self._estado} | Total: ${self._costo_total:,.2f}")
