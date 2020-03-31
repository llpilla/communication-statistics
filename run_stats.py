#!/usr/bin/env python3
"""
Communication Statistics script
Prints all statistics for a given CSV file or for a list of CSV files
Usage:
- python3 run_stats.py csvfile.csv [and other files]
- ./run_stats.py csvfile.csv [and other files]
- for computing statistics for all files in a directory: find DIR_NAME/* -exec ./run_stats.py {} +
"""

import sys
from commstats import CommunicationStatistics

def main():
    """Computes several communication statistics over a list of files"""
    for arg in sys.argv[1:]:
        print('*** Communication statistics for ' + arg + ' ***')
        stats = CommunicationStatistics(arg)
        print('Communication heterogeneity (CH):\t', stats.ch())
        print('Communication heterogeneity v2 (CH):\t', stats.ch_v2())
        print('Communication amount (CA):\t', stats.ca())
        print('Communication balance (CB):\t', stats.cb())
        print('Communication balance v2 (CB):\t', stats.cb_v2())
        print('Communication centrality (CC):\t', stats.cc())
        print('Neighbor communication factor (NBC):\t', stats.nbc())
        print('Split fraction SP(k), k=2:\t', stats.sp(2))
        print('Split fraction SP(k), k=4:\t', stats.sp(4))
        print('Split fraction SP(k), k=8:\t', stats.sp(8))
        print()

if __name__ == '__main__':
    main()
