import unittest
from indeed.anom import detect_anoms


class TestDetectAnoms(unittest.TestCase):
    def test_seasonal_data(self):
        """
        An example from real Indeed data. Numbers are the click count of one of Indeed pages.
        The last number is an anomaly caused by a holiday.
        """
        x = [534592, 854369, 868702, 852728, 773757, 618216, 423549, 497898, 836237, 883591, 888337, 818443, 660449,
             482778, 477392, 904671, 943225, 918105, 843145, 685644, 511239, 558484, 894195, 927928, 919406, 852359,
             658974, 473478, 458006, 587811]
        anoms_index = detect_anoms(x, 7)
        self.assertEqual([29], anoms_index)

    def test_twitter_data_use_r_stl(self):
        """
        Use the same R stl() function as Twitter's library. The result will be exactly the same as Twitter's.
        """
        x = []
        with open('tests/raw_data.txt', 'r') as f:
            for line in f.readlines():
                x.append(float(line))
        expected = []
        with open('tests/raw_data_expected.txt', 'r') as f:
            for line in f.readlines():
                expected.append(int(line) - 1)  # R's array index is from 1, not 0
        anoms_index = detect_anoms(x, 1440, max_anoms=0.02, direction='both', longterm_period=1440 * 14, use_r_stl=True)
        self.assertListEqual(expected, anoms_index)

    def test_twitter_data_no_r_stl(self):
        """
        Use the seasonal decomposition in python statsmodels library. Result will be slightly different from Twitter's.
        """
        x = []
        with open('tests/raw_data.txt', 'r') as f:
            for line in f.readlines():
                x.append(float(line))
        anoms_index = detect_anoms(x, 1440, max_anoms=0.02, direction='both', longterm_period=1440 * 14,
                                   use_r_stl=False)
        self.assertEqual(114, len(anoms_index))  # Twitter's result is 113

