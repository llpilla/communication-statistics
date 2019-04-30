#!/usr/bin/env python3

"""
Communication Statistics script
Prints all statistics for a given CSV file or for a list of CSV files
Usage:
- python3 runStats.py csvfile.csv [and other files]
- ./runStats.py csvfile.csv [and other files]
- for computing statistics for all files in a directory: find DIR_NAME/* -exec ./runStats.py {} +
"""

from CommunicationStatistics import CommunicationStatistics
import sys

for arg in sys.argv[1:]:
    print('*** Communication statistics for ' + arg + ' ***')
    stats = CommunicationStatistics(arg)
    print('Communication heterogeneity (CH):\t', stats.CH())
    print('Communication heterogeneity v2 (CH):\t', stats.CHv2())
    print('Communication amount (CA):\t', stats.CA())
    print('Communication balance (CB):\t', stats.CB())
    print('Communication balance v2 (CB):\t', stats.CBv2())
    print('Communication centrality (CC):\t', stats.CC())
    print('Neighbor communication factor (NBC):\t', stats.NBC())
    print('Split fraction SP(k), k=2:\t', stats.SP(2))
    print('Split fraction SP(k), k=4:\t', stats.SP(4))
    print('Split fraction SP(k), k=8:\t', stats.SP(8))
    print()

