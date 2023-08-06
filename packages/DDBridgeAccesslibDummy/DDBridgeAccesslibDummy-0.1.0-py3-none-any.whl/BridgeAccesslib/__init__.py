from .extended_comm import ExtendedBridge
import logging

logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

__author__ = "Jordi Arellano <jarellano@ifae.esm>"
__status__ = "development"
# The following module attributes are no longer updated.
__version__ = "0.0.0.1"
__date__ = "25 Oct 2022"

__all__ = {
    ExtendedBridge,
    }
