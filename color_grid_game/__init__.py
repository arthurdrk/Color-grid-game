"""
    color_grid_game package initializer
"""

import sys
import os
import numpy as np
import time
import pygame
import matplotlib.pyplot as plt
import matplotlib.colors
from collections import deque
from itertools import repeat

# type-hinting typedefs
cell = tuple[int, int]
state = list[list[int]]

# modules

from sp_utils import SPUtils
from grid import Grid

from solver import Solver
from color_grid_game.solvers import *