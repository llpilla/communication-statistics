#!/usr/bin/env python3
"""
Communication Statistics test with a 8x8 matrix with all 1s
"""

import unittest
import sys
sys.path.insert(0,'..')
from commstats import CommunicationStatistics

class allOnesTest(unittest.TestCase):
    def setUp(self):
        self.stats = CommunicationStatistics('all_1s.csv')

    def test_ch(self):
        self.assertEqual(self.stats.ch(), 0.0)

    def test_chv2(self):
        self.assertEqual(self.stats.ch_v2(), 0.0)

    def test_ca(self):
        self.assertEqual(self.stats.ca(), 1.0)

    def test_cb(self):
        self.assertEqual(self.stats.cb(), 0.0)

    def test_cbv2(self):
        self.assertEqual(self.stats.cb_v2(), 0.0)

    def test_cc(self):
        self.assertEqual(self.stats.cc(), 28./64.)

    def test_nbc(self):
        self.assertEqual(self.stats.nbc(), 1.-14./64.)

    def test_sp2(self):
        self.assertEqual(self.stats.sp(2), 0.75)

    def test_sp4(self):
        self.assertEqual(self.stats.sp(4), 0.5)

    def test_sp8(self):
        self.assertEqual(self.stats.sp(8), 0.)

if __name__ == '__main__':
    unittest.main()
