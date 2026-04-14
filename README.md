This program uses this bloom filter package

```
pip install pyprobables
```

For the data analysis, I used the holy trinity of numpy, pandas, and matplotlib
```
pip install numpy
pip install pandas
pip install matplotlib
```

To run the algorithm, run
```
python RubiksCube.py x y z
```
Substitute the command line arguments as follows:
x: heuristic to use (1-3)
y: 0 for single given scramble, 1 for single random scramble, 2 for 100 scrambles
z: if y is 0, provide the scramble. else, provide size of the scramble to look at

To generate graphs and the like using the collected data, run
```
python DataAnalysis.py
```