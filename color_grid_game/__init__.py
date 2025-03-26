"""
    color_grid_game package initializer
"""

import sys
import os
import numpy as np # type: ignore
import time
import pygame # type: ignore
import matplotlib.pyplot as plt # type: ignore
import matplotlib.colors # type: ignore
from collections.abc import Callable
from collections import deque
from itertools import repeat

# modules
from grid import Grid
from min_max_bot import Bot
from sp_utils import SPUtils

from solver import Solver
from color_grid_game.solvers import *