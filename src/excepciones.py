class ErrorSistemaFJ(Exception):
    """Excepción base para el sistema de Software FJ."""
    pass

class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados no cumplen el formato o rango."""
    pass

class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un parámetro obligatorio."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando el servicio o recurso ya se encuentra ocupado."""
    pass

class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar realizar una acción inválida sobre el estado actual."""
    pass

class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo tarifario produce valores negativos o incoherentes."""
    pass
