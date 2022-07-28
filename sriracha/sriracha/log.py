import logging
import logging.config
from functools import lru_cache


#
# Memoized to avoid unnecessary reloads
#
# See: lru_cache <https://docs.python.org/3/library/functools.html#functools.lru_cache>
#
@lru_cache
def load_config() -> None:
    config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stderr",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": [
                "console",
            ],
        },
    }

    logging.config.dictConfig(config_dict)


def get_logger(name="sriracha"):
    load_config()
    return logging.getLogger(name)
