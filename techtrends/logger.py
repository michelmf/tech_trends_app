"""
Logger to log the events in the application.

"""
import logging
import sys

from typing import Optional

def configure_logging(
        output_file: Optional[str] = None,
        logging_level:int = logging.DEBUG
    ):
    """
    Logging configuration. 
    By default, it logs to stdout and stderr.
    """
    if output_file is None:
        logging.basicConfig(
            level=logging_level,
            format='%(levelname)s:%(name)s:%(asctime)s, %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.StreamHandler(sys.stderr)
            ]
        )

    else:
        logging.basicConfig(
            filename=output_file,
            level=logging_level,
            format='%(levelname)s:%(name)s:%(asctime)s, %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S',
        )

configure_logging()