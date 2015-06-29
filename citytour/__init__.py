from .path import joke
from .path import set_city_map
from .path import set_constraints
from .path import fastest_between_nodes

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(format='%(asctime)s %(message)s')