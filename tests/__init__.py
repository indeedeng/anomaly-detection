import logging
import sys

logger = logging.getLogger('indeed')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
