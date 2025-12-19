import logging

def setup_logger(name="RAG-System"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] --- %(message)s")
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger

logger = setup_logger()
logger.info("RAG System Initialized")
