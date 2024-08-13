import logging
def set_logger():
    # Configure logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler('main.log'),
            logging.StreamHandler()
        ]
    )

    # Disable Flask's default logging for requests
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)