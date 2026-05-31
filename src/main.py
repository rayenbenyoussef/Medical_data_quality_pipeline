from src.config.logging_config import setup_logger
logger = setup_logger()


logger.info("Hello World")
logger.error("error Hello World")
logger.debug("debug Hello World")
logger.critical("critical Hello World")