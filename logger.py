import logging


def setup_logger(name: str, log_file: str, level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = setup_logger("tiktok_bot", "tiktok_run.log", level=logging.INFO)
