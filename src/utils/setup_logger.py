import logging
import platform
import sys


def setup_logger_util(name, _formatter=None):
    _logger = logging.getLogger(name)

    if platform.system() == 'Linux':
        # in prod
        level = logging.INFO
        _formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        # in dev
        level = logging.DEBUG

    if _formatter is None:
        _formatter = logging.Formatter("%(message)s")

    _stream = logging.StreamHandler(sys.stdout)
    _stream.setFormatter(_formatter)
    _logger.setLevel(level)
    if _logger.handlers == []:
        _logger.addHandler(_stream)
    return _logger
