import sys

def survivalProbability(list, input):
    out = 0
    for el in list:
        if el > input:
            out += 1
    return out / len(list)

def merl(list, input):
    l = list[:].sort()
    sv = survivalProbability(list, input) / 2
    for e in l:
        if survivalProbability(list, e) <= sv:
            return e - input

if __name__ == '__main__':

    solveTimes = []
    for i in range(3,9):
        with open(f"Results/res{i}_h1.txt") as f:
            for line in f:
                line.split