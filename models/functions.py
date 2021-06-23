from numba import njit
import numpy as np

@njit
def hi(lows_arr: np.array, highs_arr: np.array, idx_start: int = 0):
    """
    Given idx_start (and a previous high), this returns the next high, high_idx

    :param idx_start:
    :param prev_high:
    :return:
    """
    high = lows_arr[idx_start]
    high_idx = idx_start

    for idx in range(idx_start + 1, len(highs_arr)):
        act_high = highs_arr[idx]
        if act_high > high:
            high = act_high
            high_idx = idx
        else:
            return high, high_idx

    return high, high_idx

@njit
def next_hi(lows_arr: np.array, highs_arr: np.array, idx_start: int = 0, prev_high: float = 0):
    """
    Given idx_start (and a previous high), this returns the next high, high_idx

    :param idx_start:
    :param prev_high:
    :return:
    """

    high = lows_arr[idx_start]
    high_idx = None

    prev_high_reached = False
    for idx in range(idx_start + 1, len(highs_arr)):

        act_high = highs_arr[idx]

        if act_high < prev_high and not prev_high_reached:
            continue

        elif act_high > prev_high and not prev_high_reached:
            prev_high_reached = True
            high = act_high
            high_idx = idx

        elif act_high > high:
            high = act_high
            high_idx = idx

        else:
            return high, high_idx

    return None, None

@njit
def next_lo(lows_arr: np.array, highs_arr: np.array, idx_start: int, prev_low: float):
    low = highs_arr[idx_start]
    prev_low_reached = False

    for idx in range(idx_start + 1, len(lows_arr)):

        act_low = lows_arr[idx]

        if act_low > prev_low and not prev_low_reached:
            continue

        elif act_low < prev_low and not prev_low_reached:
            prev_low_reached = True
            low = act_low
            low_idx = idx

        elif act_low < low:
            low = act_low
            low_idx = idx

        else:
            return low, low_idx

    return None, None

@njit
def lo(lows_arr: np.array, highs_arr: np.array, idx_start):
    low_idx = idx_start
    low = highs_arr[idx_start]

    for idx in range(idx_start + 1, len(lows_arr)):
        act_low = lows_arr[idx]
        if act_low < low:
            low = act_low
            low_idx = idx
        else:
            return low, low_idx

    return low, low_idx