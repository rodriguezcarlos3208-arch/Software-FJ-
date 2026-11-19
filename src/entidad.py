from abc import ABC, abstractmethod
from datetime import datetime
from src.excepciones import ParametroFaltanteError

class EntidadSistema(ABC):
    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El ID de la entidad es obligatorio.")
        self._id = str(id_entidad).strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass
