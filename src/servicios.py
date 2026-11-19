from abc import abstractmethod
from src.entidad import EntidadSistema
from src.excepciones import DatosInvalidosError, ParametroFaltanteError, CalculoInconsistenteError

class Servicio(EntidadSistema):
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_hora <= 0:
            raise DatosInvalidosError(f"La tarifa por hora ({tarifa_hora}) debe ser mayor a cero.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros_especificos(self, horas: int):
        pass

    @abstractmethod
    def calcular_costo_base(self, horas: int) -> float:
        pass

    def calcular_costo_total(self, horas: int, impuesto: float = 0.19, descuento: float = 0.0, recargo: float = 0.0) -> float:
        self.validar_parametros_especificos(horas)
        base = self.calcular_costo_base(horas)
        if descuento < 0 or descuento > 0.5:
            raise CalculoInconsistenteError("El descuento debe estar entre 0% y 50%.")
        subtotal = (base - (base * descuento)) + recargo
        total = subtotal + (subtotal * impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo total calculado no puede ser menor o igual a cero.")
        return round(total, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "Ocupado"
        return f"Servicio [{self._id}] {self._nombre} | Tarifa: ${self._tarifa_hora:,.0f}/h | Estado: {estado}"


class ReservaSala(Servicio):
    CARGO_LIMPIEZA = 25000.0

    def validar_parametros_especificos(self, horas: int):
        if not isinstance(horas, int) or horas < 1 or horas > 12:
            raise DatosInvalidosError("La reserva de sala requiere entre 1 y 12 horas.")

    def calcular_costo_base(self, horas: int) -> float:
        return (self._tarifa_hora * horas) + self.CARGO_LIMPIEZA


class AlquilerEquipo(Servicio):
    def validar_parametros_especificos(self, horas: int):
        if not isinstance(horas, int) or horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo_base(self, horas: int) -> float:
        costo = self._tarifa_hora * horas
        if horas > 5:
            costo *= 0.90
        return costo


class AsesoriaEspecializada(Servicio):
    def validar_parametros_especificos(self, horas: int):
        if not isinstance(horas, int) or horas < 1 or horas > 8:
            raise DatosInvalidosError("La asesoría especializada permite sesiones de 1 a 8 horas.")

    def calcular_costo_base(self, horas: int) -> float:
        return self._tarifa_hora * horas
