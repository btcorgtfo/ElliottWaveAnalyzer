from models.MonoWave import MonoWave, MonoWaveUp  # , MonoWaveDown
import numpy as np
import unittest
from models.functions import hi, lo, next_hi, next_lo

class MonoWaveTest(unittest.TestCase):
    def test_monowave_instance_is_created(self):
        """
        This function tests whether an instance of the MonoWaveUp class is created correctly.

        Returns:
        None

        Raises:
        AssertionError: If the created object is not an instance of MonoWaveUp class.
        """

        # Generate random data for testing
        lows = np.random.rand(100)
        highs = np.random.rand(100)
        dates = np.random.rand(100)

        # Create an instance of MonoWaveUp class
        monowave_up = MonoWaveUp(lows, highs, dates, 0)

        # Check if the created object is an instance of MonoWaveUp class
        assert isinstance(monowave_up, MonoWaveUp)


class MonoWaveUpTest(unittest.TestCase):
    def setUp(self):
        # Set up test data - fully synthetic
        self.lows_arr = np.array(list([10, 8, 12, 6, 10, 4, 8, 2, 6]))
        self.highs_arr = np.array(list([20, 18, 22, 16, 20, 14, 18, 12, 16]))
        self.dates_arr = np.array(list(['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05',
                                        '2021-01-06', '2021-01-07', '2021-01-08', '2021-01-09']))
        self.idx_start = 2
        self.skip_n = 1

    def test_find_end(self):
        monowave_up = MonoWaveUp(self.lows_arr, self.highs_arr, self.dates_arr, self.idx_start, self.skip_n)
        high, high_idx = monowave_up.find_end()

        # Assert the expected high value and index
        self.assertEqual(high, 22)
        self.assertEqual(high_idx, 2)

    def test_dates_property(self):
        monowave_up = MonoWaveUp(self.lows_arr, self.highs_arr, self.dates_arr, self.idx_start, self.skip_n)
        expected_dates = ['2021-01-03', '2021-01-03']

        # Assert the expected start and end dates
        self.assertEqual(monowave_up.dates, expected_dates)

    def test_points_property(self):
        monowave_up = MonoWaveUp(self.lows_arr, self.highs_arr, self.dates_arr, self.idx_start, self.skip_n)
        expected_points = (12, 22)

        # Assert the expected low and high values
        self.assertEqual(monowave_up.points, expected_points)



if __name__ == '__main__':
    unittest.main()
