#!/bin/bash

set -x
cd tests
./unittest_all_1s.py
./unittest_100_neighbor.py
