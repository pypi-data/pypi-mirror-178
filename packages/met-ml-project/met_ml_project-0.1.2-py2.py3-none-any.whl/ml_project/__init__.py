# pylint: disable = missing-module-docstring
import sys
import logging


logger = logging.getLogger("ml_project")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s]: %(message)s"
)
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
