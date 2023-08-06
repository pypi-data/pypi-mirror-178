"""Test."""
import logging
import logging.config
import time

from logging_rate_limiter.utils import RateLimitingFilter

global log_list

log_list = list()


# here list handler is used to perform testing easily, you can use any log handler in your code
class ListHandler(logging.Handler):
    """ListHandler."""

    def __init__(self, level=logging.NOTSET, **kwargs):
        """Init."""
        super().__init__(level, **kwargs)
        self.log_list = log_list

    def emit(self, record):
        """emit."""
        self.log_list.append(record.msg)


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "list": {
            "level": "DEBUG",
            "()": ListHandler,
            "filters": ["rate_limiting_filter"]
        }
    },
    "filters": {
        "rate_limiting_filter": {
            "()": RateLimitingFilter,
            "default": {
                "tokens_per_sec": 1,
                "starting_tokens": 1,
                "max_tokens_balance": 1
            },
            "DEBUG": {
                "tokens_per_sec": 1,
                "starting_tokens": 1,
                "max_tokens_balance": 1
            },
            "result_callback": None
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["list"],
            "propagate": True
        }
    }
})

print("starting logging")
logger = logging.getLogger(__name__)


def test_logger():
    """test_logger."""
    logger.debug("test")
    assert len(log_list) == 1
    logger.debug("test")
    assert len(log_list) == 1
    logger.debug("test")
    assert len(log_list) == 1
    logger.debug("test")
    assert len(log_list) == 1
    logger.debug("test")
    assert len(log_list) == 1
    logger.debug("test")
    assert len(log_list) == 1
    time.sleep(1)
    logger.debug("test")
    assert len(log_list) == 2
    logger.info("test info")
    assert len(log_list) == 3
    logger.info("test info")
    assert len(log_list) == 3
    logger.info("test info")
    assert len(log_list) == 3
    logger.info("test info")
    assert len(log_list) == 3
    time.sleep(1)
    logger.info("test info")
    assert len(log_list) == 4
