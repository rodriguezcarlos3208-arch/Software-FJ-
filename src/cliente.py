import re
from src.entidad import EntidadSistema
from src.excepciones import DatosInvalidosError, ParametroFaltanteError

class Cliente(EntidadSistema):
    def __init__(self, id_cliente: str, nombre: str, documento: str, email: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.documento = documento
        self.email = email

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3:
            raise DatosInvalidosError(f"El nombre '{valor}' debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El documento es obligatorio.")
        doc = str(valor).strip()
        if not doc.isdigit() or len(doc) < 6:
            raise DatosInvalidosError(f"Documento inválido '{doc}'. Debe ser numérico de mínimo 6 dígitos.")
        self._documento = doc

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not valor or not valor.strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, valor.strip()):
            raise DatosInvalidosError(f"Formato de correo inválido: '{valor}'.")
        self._email = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self._id}] {self._nombre} | Doc: {self._documento} | Email: {self._email}"
