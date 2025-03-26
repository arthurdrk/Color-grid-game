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

# modules
from grid import Grid
from min_max_bot import Bot
from sp_utils import SPUtils

from solver import Solver
from color_grid_game.solvers import *