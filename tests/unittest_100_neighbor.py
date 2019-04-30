#!/usr/bin/env python3
"""
Communication Statistics test with a 8x8 matrix with all 1s
"""

import unittest
import sys
sys.path.insert(0, '..')
from commstats import CommunicationStatistics

class AllOnesTest(unittest.TestCase):
    def setUp(self):
        self.stats = CommunicationStatistics('100_neighbor.csv')

    def test_ch(self):
        self.assertEqual(self.stats.ch(), 107500./64.)

    def test_ch_v2(self):
        self.assertEqual(self.stats.ch_v2(), 10.75/64.)

    def test_ca(self):
        self.assertEqual(self.stats.ca(), 1400./64.)

    def test_cb(self):
        self.assertAlmostEqual(self.stats.cb(), (2./14.)*100., places=10)

    def test_cb_v2(self):
        self.assertAlmostEqual(self.stats.cb_v2(), 1.-14./16, places=10)

    def test_cc(self):
        self.assertAlmostEqual(self.stats.cc(), 14./64., places=10)

    def test_nbc(self):
        self.assertEqual(self.stats.nbc(), 0.)

    def test_sp2(self):
        self.assertAlmostEqual(self.stats.sp(2), 1.-8./14., places=10)

    def test_sp4(self):
        self.assertAlmostEqual(self.stats.sp(4), 1.-12./14., places=10)

    def test_sp8(self):
        self.assertEqual(self.stats.sp(8), 0.)

if __name__ == '__main__':
    unittest.main()
