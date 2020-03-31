#!/usr/bin/env python3
"""
Communication Statistics script
Reads multiple CSV files to generate a single CSV file with multiple statistics
Usage:
- python3 run_muliple.py input_file output_file.csv
- ./run_multiple.py input_file output_file.csv]
The input file is composed of one or more lines. 
Each line contains the path to a CSV input file and the application's name.
"""

import sys
import pandas as pd
from commstats import CommunicationStatistics

def main():
    """Computes several communication statistics over a list of files"""
    # Reads the input file
    # each row: path to a communication matrix file, application name
    inputs = pd.read_csv(sys.argv[1], delimiter=",", header=None)
    output_df = pd.DataFrame(columns=['Application','CH','CHv2','CA','CB','CBv2',
                                      'CC','NBC','SP(4)','SP(16)'])
    # Iterate over rows
    for index, row in inputs.iterrows():
        # row[0]: file
        # row[1]: application name
        stats = CommunicationStatistics(row[0])
        # computes all stats and adds as a row in the output DataFrame
        output_df = output_df.append({
            'Application': row[1],
            'CH': stats.ch(),
            'CHv2': stats.ch_v2(),
            'CA': stats.ca(),
            'CB': stats.cb(),
            'CBv2': stats.cb_v2(),
            'CC': stats.cc(),
            'NBC': stats.nbc(),
            'SP(4)': stats.sp(4),
            'SP(16)': stats.sp(16),
        }, ignore_index=True)
    # Saves output DataFrame as a CSV file
    output_df.to_csv(sys.argv[2], sep=',', index=False)

if __name__ == '__main__':
    main()
