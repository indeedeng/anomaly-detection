import unittest
from tests.anoms_test import read_twitter_raw_data
from breakout import detect_breakout
import numpy as np


class TestBreakoutDetection(unittest.TestCase):
    def setUp(self):
        self.data = read_twitter_raw_data('tests/scribe_data.txt')

    def test_edm_multi(self):
        ret_list = detect_breakout(self.data, min_size=24, method='multi', beta=0.001, degree=1)
        self.assertEqual([47, 87], ret_list)

    def test_edm_percent(self):
        ret_list = detect_breakout(self.data, min_size=24, method='multi', percent=0.1, degree=1)
        self.assertEqual([26, 51, 106], ret_list)

    def test_edm_x_no_nperm(self):
        ret_list = detect_breakout(self.data, min_size=24, method='amoc', exact=True, sig_level=0.05, nperm=0)
        self.assertEqual([95], ret_list)

    def test_edm_x_nperm_has_ret(self):
        ret_list = detect_breakout(self.data, min_size=24, method='amoc', exact=True, sig_level=0.9, nperm=10)
        self.assertEqual([95], ret_list)

    def test_edm_x_nperm_no_ret(self):
        ret_list = detect_breakout(self.data, min_size=24, method='amoc', exact=True, sig_level=0.001, nperm=10)
        self.assertEqual([], ret_list)

    def test_edm_tail_no_nperm(self):
        ret_list = detect_breakout(self.data, min_size=24, method='amoc', exact=False, sig_level=0.05, nperm=0)
        self.assertEqual([47], ret_list)

    def test_edm_tail_nperm_has_ret(self):
        ret_list = detect_breakout(self.data, min_size=24, method='amoc', exact=False, sig_level=0.9, nperm=10)
        self.assertEqual([47], ret_list)

    def test_edm_tail_nperm_no_ret(self):
        ret_list = detect_breakout(self.data, min_size=24, method='amoc', exact=False, sig_level=0.001, nperm=10)
        self.assertEqual([], ret_list)

    def test_invalid_parameters(self):
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=0,
                          method='amoc', exact=False, sig_level=0.001, nperm=10)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=1.5,
                          method='amoc', exact=False, sig_level=0.001, nperm=10)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, alpha=0, sig_level=0.001, nperm=10)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, alpha=2.1, sig_level=0.001, nperm=10)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, sig_level=0.0, nperm=10)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, sig_level=1.0, nperm=10)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, sig_level=0.001, nperm=-1)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, sig_level=0.001, nperm=1.1)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='multi', beta=0.008, degree=3)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='multi', degree=0)
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='wrong_method', exact=False, sig_level=0.001, nperm=10)

    def test_empty(self):
        ret_list = detect_breakout([], min_size=24, method='multi', beta=0.001, degree=1)
        self.assertEqual([], ret_list)

    def test_constant(self):
        ret_list = detect_breakout([10] * 100, min_size=24, method='multi', beta=0.001, degree=1)
        self.assertEqual([], ret_list)

    def test_nan(self):
        self.data[10] = np.nan
        self.assertRaises(ValueError, detect_breakout, self.data, min_size=30,
                          method='amoc', exact=False, sig_level=0.001, nperm=10)

    def test_int_values(self):
        # make sure the code still works if the values are int.
        z = [int(value) for value in self.data]
        ret_list = detect_breakout(z, min_size=24, method='multi', beta=0.001, degree=1)
        self.assertEqual([47, 87], ret_list)
