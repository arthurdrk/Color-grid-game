"""
    color_grid_game package initializer
"""

import sys
import os
import numpy as np
import time
import pygame
from collections import deque
from itertools import repeat


# type-hinting typedefs
cell = tuple[int, int]
state = list[list[int]]

# modules
from swap_puzzle.exception import *
from sp_utils import SPUtils
from graph import Graph
from grid import Grid

from solver import Solver
from swap_puzzle.solvers import *