from src.gestor import GestorSoftwareFJ
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.excepciones import ErrorSistemaFJ
from src.logger import obtener_logger

def ejecutar_simulacion():
    logger = obtener_logger()
    gestor = GestorSoftwareFJ()
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===\n")

    c1 = gestor.registrar_cliente("C01", "Laura Martínez", "1110456789", "laura.martinez@correo.com")
    c2 = gestor.registrar_cliente("C02", "Carlos Gómez", "1110987654", "carlos.gomez@empresa.co")

    gestor.registrar_cliente("C03", "Andrés Ruiz", "1110222333", "correo_sin_arroba.com")
    gestor.registrar_cliente("C04", "María López", "1110456789", "maria.lopez@correo.com")

    sala = ReservaSala("S01", "Sala de Juntas Ejecutiva", 80000)
    equipo = AlquilerEquipo("S02", "Workstation Portátil Core i9", 35000)
    asesoria = AsesoriaEspecializada("S03", "Consultoría Arquitectura Cloud", 120000)
    gestor.agregar_servicio(sala)
    gestor.agregar_servicio(equipo)
    gestor.agregar_servicio(asesoria)

    try:
        servicio_invalido = ReservaSala("S04", "Sala Defectuosa", -50000)
        gestor.agregar_servicio(servicio_invalido)
    except ErrorSistemaFJ as e:
        logger.error(f"Fallo al instanciar servicio S04: {e}")
        print(f"[ERROR CONTROLADO] Servicio S04: {e}")

    r1 = gestor.crear_y_confirmar_reserva("R01", c1, sala, 4)
    gestor.crear_y_confirmar_reserva("R02", c2, sala, 2)
    gestor.crear_y_confirmar_reserva("R03", c2, equipo, 1)
    gestor.crear_y_confirmar_reserva("R04", c2, equipo, 6, descuento=0.05)
    gestor.crear_y_confirmar_reserva("R05", c1, asesoria, 3)

    gestor.cancelar_reserva(r1)
    gestor.crear_y_confirmar_reserva("R06", c2, sala, 3)
    gestor.cancelar_reserva(r1)

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revise el archivo 'sistema_software_fj.log' para ver la auditoría completa.")

if __name__ == "__main__":
    ejecutar_simulacion()
