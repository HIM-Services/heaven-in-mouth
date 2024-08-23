import unittest
import os
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


class TestLogger(unittest.TestCase):

    def setUp(self):
        set_logger()

    def test_logging_to_file(self):
        logging.warning('This is a test warning')

        self.assertTrue(os.path.exists('main.log'))

        with open('main.log', 'r') as log_file:
            log_content = log_file.read()
            self.assertIn('This is a test warning', log_content)

    def tearDown(self):
        if os.path.exists('main.log'):
            os.remove('main.log')


if __name__ == '__main__':
    unittest.main()
