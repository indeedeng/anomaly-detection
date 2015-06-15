import unittest
from indeed.anom import detect_anoms


class TestDetectAnoms(unittest.TestCase):
    def test_seasonal_data(self):
        x = [534592, 854369, 868702, 852728, 773757, 618216, 423549, 497898, 836237, 883591, 888337, 818443, 660449,
             482778, 477392, 904671, 943225, 918105, 843145, 685644, 511239, 558484, 894195, 927928, 919406, 852359,
             658974, 473478, 458006, 587811]
        anoms_index = detect_anoms(x, 7)
        self.assertEqual([29], anoms_index)

    def test_twitter_data(self):
        x = []
        with open('tests/raw_data.txt', 'r') as f:
            for line in f.readlines():
                x.append(float(line))
        anoms_index = detect_anoms(x, 1440, max_anoms=0.02, direction='both', longterm_period=1440 * 14)
        self.assertEqual([], anoms_index, msg=str(len(anoms_index)) + str(anoms_index))

