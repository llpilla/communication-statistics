#!/usr/bin/env python3
"""
Communication Statistics test with a 8x8 matrix with all 1s
"""

import unittest
import sys
sys.path.insert(0,'..')
from CommunicationStatistics import CommunicationStatistics

class allOnesTest(unittest.TestCase):
    def setUp(self):
        self.stats = CommunicationStatistics('all_1s.csv')

    def test_CH(self):
        self.assertEqual(self.stats.CH(),0.0)

    def test_CHv2(self):
        self.assertEqual(self.stats.CHv2(),0.0)

    def test_CA(self):
        self.assertEqual(self.stats.CA(),1.0)

    def test_CB(self):
        self.assertEqual(self.stats.CB(),0.0)

    def test_CBv2(self):
        self.assertEqual(self.stats.CBv2(),0.0)

    def test_CC(self):
        self.assertEqual(self.stats.CC(),28./64.)

    def test_NBC(self):
        self.assertEqual(self.stats.NBC(),1.-14./64.)

    def test_SP2(self):
        self.assertEqual(self.stats.SP(2),0.75)

    def test_SP4(self):
        self.assertEqual(self.stats.SP(4),0.5)

    def test_SP8(self):
        self.assertEqual(self.stats.SP(8),0.)

if __name__ == '__main__':
    unittest.main()

