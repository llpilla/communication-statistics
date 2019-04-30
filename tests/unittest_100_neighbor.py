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
        self.stats = CommunicationStatistics('100_neighbor.csv')

    def test_CH(self):
        self.assertEqual(self.stats.CH(),107500./64.)

    def test_CHv2(self):
        self.assertEqual(self.stats.CHv2(),10.75/64.)

    def test_CA(self):
        self.assertEqual(self.stats.CA(),1400./64.)

    def test_CB(self):
        self.assertAlmostEqual(self.stats.CB(),(2./14.)*100., places=10)

    def test_CBv2(self):
        self.assertAlmostEqual(self.stats.CBv2(),1.-14./16, places=10)

    def test_CC(self):
        self.assertAlmostEqual(self.stats.CC(),14./64., places=10)

    def test_NBC(self):
        self.assertEqual(self.stats.NBC(),0.)

    def test_SP2(self):
        self.assertAlmostEqual(self.stats.SP(2),1.-8./14., places=10)

    def test_SP4(self):
        self.assertAlmostEqual(self.stats.SP(4),1.-12./14., places=10)

    def test_SP8(self):
        self.assertEqual(self.stats.SP(8),0.)

if __name__ == '__main__':
    unittest.main()

