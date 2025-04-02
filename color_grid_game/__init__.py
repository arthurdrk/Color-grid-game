"""
    color_grid_game package initializer
"""

import sys
import os
import numpy as np # type: ignore
import networkx as nx
import argparse
import time
import matplotlib.pyplot as plt # type: ignore
import matplotlib.colors # type: ignore
from collections.abc import Callable
from collections import deque 
from collections import defaultdict
from itertools import repeat

# modules
from .grid import Grid
from .min_max_bot import Bot
from .solver import Solver
from .solvers import *