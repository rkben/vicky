import logging
import sys

import bot
from loguru import logger
from settings import settings

LOG_LEVEL = logging.getLevelName("INFO")
if settings.DEBUG:
    LOG_LEVEL = logging.getLevelName("DEBUG")

JSON_LOGS = False
if settings.JSON_LOGS:
    JSON_LOGS = True


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


if __name__ == "__main__":
    _setup_logging()
    bot.run()
