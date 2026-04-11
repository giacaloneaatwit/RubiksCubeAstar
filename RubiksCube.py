"""
Command Line arguments:
python RubiksCube.py a b c
a: heuristic to use
b: 0 for single given scramble, 1 for single random scramble, 2 for doing the 100 scrambles, 3 is used for testing things
c: if b is 0, provide the scramble. else, provide size of the scramble to look at
"""

import random
import time
import sys
from queue import PriorityQueue
from itertools import count
from bloomfilter import BloomFilter

shuffleSize = 0
if int(sys.argv[2]) == 1 or int(sys.argv[2]) == 2:
    shuffleSize = int(sys.argv[3])
heuristic = int(sys.argv[1])
maxDepth = 7
iterator = (count(start = 0, step = 1))

class Rubik:
    """
    CUBE NET
        444
        4E4
        444
    000 111 222 333
    0A0 1B1 2C2 3D3
    000 111 222 333
        555
        5F5
        555

    face order
    012
    7_3
    654

    dir
     1
    4 2
     3
    """
    solved = "000000001111111122222222333333334444444455555555"
    numGenerated = 0
    numExpanded = 0

    def __init__(self, state="000000001111111122222222333333334444444455555555", path=""):
        self.state = state
        self.path = path
        Rubik.numGenerated += 1
    
    def getState(self):
        return self.state
    
    def getPath(self):
        return self.path

    def stateDepth(self):
        return len(self.path)
    
    def updateFace(self, face, newf):
        """Given a new face, change the cube state to adjust the new face"""
        out = ""
        if face > 0:
            out += self.state[:face*8]
        out += newf
        if face < 5:
            out += self.state[face*8+8:]
        
        self.state = out
    
    def getEdge(self, face, dir):
        f = self.state[face*8:face*8 + 8]
        out = ""
        match dir:
            case 1:
                out = f[0:3]
            case 2:
                out = f[2:5]
            case 3:
                out = f[4:7]
            case 4:
                out = f[-2:] + f[0]
        return out

    def setEdge(self, face, dir, input):
        f = self.state[face*8:face*8+8]
        match dir:
            case 1:
                f = input + f[3:]
            case 2:
                f = f[:2] + input + f[5:]
            case 3:
                f = f[:4] + input + f[7]
            case 4:
                f = input[2] + f[1:6] + input[:2]
        
        self.updateFace(face, f)
    
    def turn(self, move):
        dir = move.isupper()
        face = ord(move.lower())-ord('a')

        f = self.state[face*8:face*8+8]
        if dir: #clockwise
            temp = f[6:8]
            f = temp[:7] + f[:6]
        else:
            temp = f[:2]
            f = f[2:] + temp
        
        self.updateFace(face, f)

        edges = []
        match face:
            case 0:
                edges = [
                    Edge(1, 4, self.getEdge(1,4)),
                    Edge(5, 4, self.getEdge(5,4)),
                    Edge(3, 2, self.getEdge(3,2)),
                    Edge(4, 4, self.getEdge(4,4))
                ]
            case 1:
                edges = [
                    Edge(2, 4, self.getEdge(2,4)),
                    Edge(5, 1, self.getEdge(5,1)),
                    Edge(0, 2, self.getEdge(0,2)),
                    Edge(4, 3, self.getEdge(4,3))
                ]
            case 2:
                edges = [
                    Edge(3, 4, self.getEdge(3,4)),
                    Edge(5, 2, self.getEdge(5,2)),
                    Edge(1, 2, self.getEdge(1,2)),
                    Edge(4, 2, self.getEdge(4,2))
                ]
            case 3:
                edges = [
                    Edge(0, 4, self.getEdge(0,4)),
                    Edge(5, 3, self.getEdge(5,3)),
                    Edge(2, 2, self.getEdge(2,2)),
                    Edge(4, 1, self.getEdge(4,1))
                ]
            case 4:
                edges = [
                    Edge(2, 1, self.getEdge(2,1)),
                    Edge(1, 1, self.getEdge(1,1)),
                    Edge(0, 1, self.getEdge(0,1)),
                    Edge(3, 1, self.getEdge(3,1))
                ]
            case 5:
                edges = [
                    Edge(2, 3, self.getEdge(2,3)),
                    Edge(3, 3, self.getEdge(3,3)),
                    Edge(0, 3, self.getEdge(0,3)),
                    Edge(1, 3, self.getEdge(1,3))
                ]
        for i in range(len(edges)):
            idxTo = i
            if dir:
                idxTo += 1
                idxTo %= 4
            else:
                idxTo -= 1
            self.setEdge(edges[idxTo].face, edges[idxTo].dir, edges[i].edge)

    def shuffle(self, path):
        for char in path:
            self.turn(char)
        return path
    
    def scramble(self, length):
        moves = "AaBbCcDdEeFf"
        path = ""
        for i in range(length):
            path += moves[random.randint(0,11)]
        self.shuffle(path)
        return path

    def isSolved(self):
        return self.state == Rubik.solved
    
    def faceToString(self, face):
        f = self.state[face*8:face*8 + 8]
        return f[:3] + f[7] + str(face) + f[3] + f[6:3:-1]
    
    def printCube(self):
        str = "Path: " + self.path + "\n"
        for i in range(3):
            str += "    " + self.faceToString(4)[3*i:3*i+3] + "\n"
        for i in range(3):
            str += self.faceToString(0)[3*i:3*i+3] + " " + self.faceToString(1)[3*i:3*i+3] + " " + self.faceToString(2)[3*i:3*i+3] + " " + self.faceToString(3)[3*i:3*i+3] + "\n"
        for i in range(3):
            str += "    " + self.faceToString(5)[3*i:3*i+3] + "\n"
        print(str)
        

class Edge:
    def __init__(self, face, dir, edge):
        self.face = face
        self.dir = dir
        self.edge = edge

#heuristics
def h1(cube: Rubik): # number of squares in the wrong place
    count = 0
    for i in range(48):
        square = int(cube.state[i])
        if not square == i // 8:
            count += 1
    return cube.stateDepth() + count
def h2(cube: Rubik): # counting the absolute difference bewtween squares
    count = 0
    for i in range(47):
        count += abs(int(cube.state[i+1]) - int(cube.state[i]))
    return cube.stateDepth() + count
def h3(cube: Rubik): # number of edge and corner pieces that are in the wrong place
    countEdge = 0
    countCorner = 0
    for i in range(48):
        square = int(cube.state[i])
        if not square == i // 8:
            if i % 2 == 0:
                countCorner += 1
            else:
                countEdge += 1
    return cube.stateDepth() + countEdge/2 + countCorner/3
def h(heuristic):
    if heuristic == 1:
        return h1
    elif heuristic == 2:
        return h2
    elif heuristic == 3:
        return h3
    else:
        return

def cycleCheck(cube: Rubik, expanded, bloom):
    if not cube.getState() in bloom:
        return False
    return True
    for ex in expanded:
        if cube.getState() == ex:
            return True
    return False

def expand(cube: Rubik, queue: PriorityQueue, h):
    if cube.stateDepth() >= maxDepth:
        return
    for char in "AaBbCcDdEeFf":
        #don't consider moves that just undo the previous move
        if cube.stateDepth() > 0:
            if char.isupper() == cube.getPath()[-1].islower() and char.lower() == cube.getPath()[-1].lower():
                continue
        
        newCube = Rubik(cube.getState(), cube.getPath())
        newCube.path += char
        newCube.turn(char)

        queue.put( (h(newCube), next(iterator), newCube) )
    Rubik.numExpanded += 1
    print(f"\r{Rubik.numExpanded} states expanded so far", end="", flush=True)

def astar(cube, h):
    frontier = PriorityQueue()
    frontier.put( (h(cube), next(iterator), cube) )
    expanded = []
    bloomFilter = BloomFilter(expected_insertions=1000000000, err_rate=0.000000001)

    while not frontier.empty():
        priority, counter, c = frontier.get()
        if c.isSolved():
            return c
        
        if cycleCheck(c, expanded, bloomFilter):
            continue

        expand(c, frontier, h)
        bloomFilter.put(c.getState())
        #expanded.append(c.getState())
    return None

if __name__ == '__main__':
    if int(sys.argv[2]) == 0: # solve a single given scramble
        cube = Rubik()

        scram = cube.shuffle(sys.argv[3])
        print("Scramble: " + scram)
        cube.printCube()

        startTime = time.perf_counter()
        res = astar(cube, h(heuristic))
        endTime = time.perf_counter()
        elapsedTime = endTime - startTime

        if res is None:
            print("Cube Failed")
        else:
            res.printCube()
        print(f"Number of states generated: {Rubik.numGenerated}")
        print(f"Number of states expanded: {Rubik.numExpanded}")
        print(f"Time elapsed: {elapsedTime:.2f} seconds")

    elif int(sys.argv[2]) == 1: # solve a single random scramble
        cube = Rubik()

        scram = cube.scramble(shuffleSize)
        print("Scramble: " + scram)
        cube.printCube()

        startTime = time.perf_counter()
        res = astar(cube, h(heuristic))
        endTime = time.perf_counter()
        elapsedTime = endTime - startTime

        print("")
        if res is None:
            print("Cube Failed")
        else:
            res.printCube()
        print(f"Number of states generated: {Rubik.numGenerated}")
        print(f"Number of states expanded: {Rubik.numExpanded}")
        print(f"Time elapsed: {elapsedTime:.2f} seconds")

    elif int(sys.argv[2]) == 2: # solve the 100 scrambles 
        scrambles = []
        with open(f"Scrambles/scram{shuffleSize}.txt") as f:
            scrambles = [line.strip() for line in f]
        
        #with open("Scrambles/CollisionTest.txt") as f:
        #    scrambles = [line.strip() for line in f]

        solveTimes = []
        numExp = []
        numGen = []
        numFailed = 0
        for i, scramble in enumerate(scrambles):
            Rubik.numExpanded = 0
            Rubik.numGenerated = 0
            cube = Rubik()
            cube.shuffle(scramble)

            startTime = time.perf_counter()
            res = astar(cube, h(heuristic))
            endTime = time.perf_counter()
            elapsedTime = endTime - startTime

            solveTimes.append(elapsedTime)
            numExp.append(Rubik.numExpanded)
            numGen.append(Rubik.numGenerated)
            if res is None:
                print(f"Failed {i}: {scramble} in {elapsedTime:.2f} seconds. {Rubik.numExpanded} states expanded. {Rubik.numGenerated} states generated")
                numFailed += 1
            else:
                #pass
                print(f"Completed {i}: {scramble} in {elapsedTime:.2f} seconds. {Rubik.numExpanded} states expanded. {Rubik.numGenerated} states generated")
            #print(f"\rCompleted {i}: {scramble} in {elapsedTime:.2f} seconds. {Rubik.numExpanded} states expanded. {Rubik.numGenerated} states generated----------------", end="", flush=True)
        print("")
        avgTime = sum(solveTimes) / len(solveTimes)
        avgExp = sum(numExp) / len(numExp)
        avgGen = sum(numGen) / len(numGen)
        print(f"DEPTH OF {shuffleSize} WITH h{heuristic} COMPLETE!\nAverage Time: {avgTime:.2f}\nAverage Number of States Expanded: {avgExp}\nAverage Number of States Generated: {avgGen}")
        print(f"{numFailed} failed.")
    
    elif int(sys.argv[2]) == 3: #used for testing things without messing with the other paths
        cube = Rubik()

        scram = cube.shuffle(sys.argv[3])
        print("Scramble: " + scram)
        cube.printCube()
        print(f"H1: {h1(cube)}\nH2: {h2(cube)}\nH3: {h3(cube)}\n")

        for i in range(len(sys.argv[3])):
            cube.turn(sys.argv[3][len(sys.argv[3])-i-1])
            cube.turn(sys.argv[3][len(sys.argv[3])-i-1])
            cube.turn(sys.argv[3][len(sys.argv[3])-i-1])
            print(cube.getState())
            
            #cube.printCube()
            #print(f"H1: {h1(cube)}\nH2: {h2(cube)}\nH3: {h3(cube)}\n")
        