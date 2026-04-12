#!/bin/bash

for i in {3..8}; do
    python RubiksCube.py $1 2 $i | tee -a "Results/res${i}_h$1.csv"
done