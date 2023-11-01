import logging as log
import numpy as np
from ortools.linear_solver import pywraplp

# Setting up logger
for handler in log.root.handlers[:]:
    log.root.removeHandler(handler)
log.basicConfig(format="%(levelname)s - %(message)s")

logger = log.getLogger()
logger.setLevel(log.DEBUG)
log.info("Logger initialized...")
