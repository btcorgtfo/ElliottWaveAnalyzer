from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Union
from abc import ABC, abstractmethod
from numba import njit, vectorize
from numba.experimental import jitclass







class WaveOptions:
    def __init__(self, i: int, j: int = None, k: int = None, l: int = None, m: int = None):
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.m = m

    @property
    def values(self):
        if self.k is not None:
            return [self.i, self.j, self.k, self.l, self.m]
        else:
            return [self.i, self.j]

    def __hash__(self):
        if self.k is not None:
            hash_str = f'{self.i}_{self.j}_{self.k}_{self.l}_{self.m}'
        else:
            hash_str = f'{self.i}_{self.j}'
        return hash(hash_str)

    def __eq__(self, other):
        if self.k is not None:
            if self.i == other.i and self.j == other.j and self.k == other.k and self.l == other.l and self.m == other.m:
                return True
            else:
                return False
        else:
            if self.i == other.i and self.j == other.j:
                return True
            else:
                return False
