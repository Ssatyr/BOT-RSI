import logging
import logging.handlers

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # This sets the lowest level of logging for the logger itself

    # Create a file handler that logs debug and higher level messages
    file_handler = logging.handlers.RotatingFileHandler(
        'my_app.log', maxBytes=1048576, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)  # File handler level

    # Create console handler that logs error and higher level messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # Console handler level

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
