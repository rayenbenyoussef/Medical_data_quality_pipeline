import logging
import os
import sys

def setup_logger():
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    # 🔥 ROOT du projet (remonte de src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    Gformatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    Dformatter = logging.Formatter(
        '[%(levelname)s:%(levelno)s] %(asctime)s - %(message)s\n%(pathname)s - %(funcName)s - %(lineno)d\n')

    class InfoHandler(logging.Filter):
        def filter(self, record):
            return record.levelno == logging.INFO or record.levelno == logging.WARNING

    info_handler = logging.FileHandler(
        os.path.join(logs_dir, "pipeline.log"),
        encoding="utf-8",
        mode="w"
    )
    info_handler.addFilter(InfoHandler())
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(Gformatter)

    error_handler = logging.FileHandler(
        os.path.join(logs_dir, "errors.log"),
        encoding="utf-8",
        mode="w"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(Gformatter)

    debug_handler = logging.FileHandler(
        os.path.join(logs_dir, "debug.log"),
        encoding="utf-8",
        mode="w"
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(Dformatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Gformatter)

    logger.addHandler(console_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(debug_handler)

    return logger
