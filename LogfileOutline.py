import logging
import os
import unittest


def setup_logger(logfile_name='application.log'):
    # Check if logfile already exists
    file_exists = os.path.isfile(logfile_name)

    # Set up the logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(logfile_name),
            logging.StreamHandler()
        ]
    )

    # If the logfile already exists, log a message indicating it's being appended
    if file_exists:
        logging.info('Logfile exists, appending new entries.')
    else:
        logging.info('Creating new logfile.')

#Code for checking the log manually
#Can also use this as a outline for incorporating into functions
def test_logging():
    setup_logger()
    logging.info('Testing log entry: Application started.')
    logging.warning('Testing log entry: Warning example.')
    logging.error('Testing log entry: Error example.')

if __name__ == "__main__":
    test_logging()


# Class to check for logging automatically
class TestLoggingFunction(unittest.TestCase):
    def test_logging_output(self):
        logfile_name = 'test_application.log'
        setup_logger(logfile_name)
        logging.info('Test log entry: ')

        with open(logfile_name, 'r') as log_file:
            log_content = log_file.read()

        self.assertIn('Test log entry', log_content)
if __name__ == "__name__":
    unittest.main()

#Code to clear previous automatic test log
def cleanup_logfile(logfile_name='test_application.log'):
    if os.path.isfile(logfile_name):
        os.remove(logfile_name)
        print(f"Logfile '{logfile_name}' removed after test")

cleanup_logfile()
