import logging
from logging.handlers import RotatingFileHandler

name = 'app'

logger = logging.getLogger(name)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    'logs/weather.log', 
    maxBytes=1024*1024,
    backupCount=5
)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)
logger.propagate = False