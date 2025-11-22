import logging
import sys
from config import LOG_LEVEL

def setup_logger(name="MarketPulse"):
    """Sets up a logger with the specified name and log level."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler('marketpulse.log')
    
    c_handler.setLevel(getattr(logging, LOG_LEVEL.upper()))
    f_handler.setLevel(getattr(logging, LOG_LEVEL.upper()))

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
