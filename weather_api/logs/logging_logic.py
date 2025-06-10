import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        'logs/weather.log', 
        maxBytes=1024*1024,
        backupCount=5
    )
    console_handler = logging.StreamHandler()

    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger