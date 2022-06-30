import logging
import os


def get_logger(name="sriracha"):
    log = logging.getLogger(name)
    log.setLevel(level=logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    log.addHandler(ch)
    return log
