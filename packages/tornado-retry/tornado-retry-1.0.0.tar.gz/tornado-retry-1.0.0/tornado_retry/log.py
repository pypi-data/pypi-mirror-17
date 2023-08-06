import logging

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())
logger.setLevel(logging.ERROR)


__all__ = [
    'logger',
]
