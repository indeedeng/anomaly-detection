import unittest
from anoms import detect_anoms


# Test that we can get exactly the same result as Twitter's AnomalyDetection library.
# The 'raw_data.txt' is containing the same data as 'raw_data.R'.
# The expected_*.txt files are containing the same result from 'vec_anom_detection.R' using same parameters.
def _read_twitter_raw_data(filename):
    x = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            x.append(float(line))
    return x


def _read_twitter_test_result(filename):
    expected = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            expected.append(int(line) - 1)  # R's array index is from 1, not 0
    return expected


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

    def test_twitter_data_regular(self):
        """
        Use the same test data from Twitter's library. The result will be exactly the same as Twitter's.
        """
        x = _read_twitter_raw_data('tests/raw_data.txt')
        expected = _read_twitter_test_result('tests/expected_regular.txt')
        ret = detect_anoms(x, 1440, max_anoms=0.02, direction='both', longterm_period=1440 * 14)
        self.assertListEqual(expected, ret)
