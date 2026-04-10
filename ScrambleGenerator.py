import sys
import random

if __name__ == "__main__":
    scrambleSize = int(sys.argv[1])
    numGen = int(sys.argv[2])
    filePath = sys.argv[3]

    moveList = "ABCDEFabcdef"
    moves = []
    for i in range(numGen):
        st = ""
        for j in range(scrambleSize):
            st += moveList[random.randint(0,11)]
        moves.append(st)
    
    with open(filePath, "w") as f:
        for scramble in moves:
            print(scramble, file=f)