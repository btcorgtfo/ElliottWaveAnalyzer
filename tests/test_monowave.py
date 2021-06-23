from models.MonoWave import MonoWaveUp
import numpy as np


def test_monowave_instance_is_created():
    lows = np.random.rand(100)
    highs = np.random.rand(100)
    dates = np.random.rand(100)

    monowave_up = MonoWaveUp(lows, highs, dates, 0)

    assert isinstance(monowave_up, MonoWaveUp)