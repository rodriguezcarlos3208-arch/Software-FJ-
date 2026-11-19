from src.cliente import Cliente
from src.servicios import Servicio
from src.reserva import Reserva
from src.excepciones import ErrorSistemaFJ, DatosInvalidosError, OperacionNoPermitidaError
from src.logger import obtener_logger

class GestorSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._logger = obtener_logger()

    def registrar_cliente(self, id_cliente: str, nombre: str, documento: str, email: str):
        try:
            if any(c.documento == str(documento).strip() for c in self._clientes):
                raise DatosInvalidosError(f"Ya existe un cliente registrado con el documento {documento}.")
            nuevo_cliente = Cliente(id_cliente, nombre, documento, email)
        except ErrorSistemaFJ as e:
            self._logger.error(f"Fallo al registrar cliente ({id_cliente}): {e}")
            print(f"[ERROR CONTROLADO] Cliente {id_cliente}: {e}")
            return None
        else:
            self._clientes.append(nuevo_cliente)
            self._logger.info(f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        finally:
            self._logger.info(f"Finalizado intento de registro de cliente {id_cliente}.")

    def agregar_servicio(self, servicio_obj: Servicio):
        self._servicios.append(servicio_obj)
        self._logger.info(f"Servicio catalogado: {servicio_obj.obtener_resumen()}")
        print(f"[OK] {servicio_obj.obtener_resumen()}")

    def crear_y_confirmar_reserva(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int, descuento: float = 0.0):
        try:
            if cliente is None or servicio is None:
                raise OperacionNoPermitidaError("No se puede crear reserva con cliente o servicio nulo.")
            reserva = Reserva(id_reserva, cliente, servicio, horas)
            reserva.confirmar(descuento=descuento)
        except ErrorSistemaFJ as e:
            try:
                raise OperacionNoPermitidaError(f"Fallo en el procesamiento de reserva {id_reserva}") from e
            except OperacionNoPermitidaError as err_encadenado:
                causa = err_encadenado.__cause__
                self._logger.error(f"{err_encadenado} | Causa raíz: {causa}")
                print(f"[ERROR ENCADENADO] {err_encadenado} -> Motivo: {causa}")
                return None
        else:
            self._reservas.append(reserva)
            self._logger.info(f"Reserva confirmada: {reserva.obtener_resumen()}")
            print(f"[OK] {reserva.obtener_resumen()}")
            return reserva

    def cancelar_reserva(self, reserva: Reserva):
        try:
            if reserva is None:
                raise OperacionNoPermitidaError("La reserva indicada no existe.")
            reserva.cancelar()
        except ErrorSistemaFJ as e:
            self._logger.error(f"Error al cancelar reserva: {e}")
            print(f"[ERROR CONTROLADO] Cancelación fallida: {e}")
        else:
            self._logger.info(f"Reserva cancelada y recurso liberado: {reserva.obtener_resumen()}")
            print(f"[OK] {reserva.obtener_resumen()}")
