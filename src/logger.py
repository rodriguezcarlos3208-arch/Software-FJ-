import logging

def obtener_logger():
    logger = logging.getLogger("SoftwareFJ")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_handler = logging.FileHandler("sistema_software_fj.log", mode="w", encoding="utf-8")
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)
    return logger
