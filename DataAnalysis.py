import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# median residual lifetime. finds the expected remaining time to an event given a sample has survived up to a given point already
def merl(data, h, column, input): 
    s = data[8][h][column]
    survived = s[s >= input]
    return survived.median() - input

def makeMERLchart(data, column, bounds, log, title, xlabel, ylabel):
    xAxis = []
    if log:
        xAxis = np.logspace(bounds[0], bounds[1], 50)
        plt.yscale("log")
        plt.xscale("log")
    else:
        xAxis = [i for i in range(bounds[0],bounds[1])]
    for h in range(1,4):
        plt.plot(xAxis, [merl(data,h, column, i) for i in xAxis], label=f"h{h}")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def makeLineChart(data, column, title, xlabel, ylabel):
    for j in range(1,4):
        depths = [3,4,5,6,7,8]
        times = []
        stdev = []
        for depth in depths:
            times.append( sum(list(data[depth][j][column]))/100 )
            stdev.append( data[depth][j][column].std() )
        plt.plot(depths,times, label=f"h{j}")
        #plt.errorbar(depths, times, yerr=stdev, fmt='o', capsize=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def makeHistogram(data, column, h, bounds, density, title, xlabel, ylabel):
    plt.hist(data[8][h][column], bins=np.logspace(bounds[0], bounds[1], density), edgecolor='black')
    plt.xscale('log')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show()

if __name__ == '__main__':
    data = [[None for i in range(4)] for j in range(9)] # data[depth][heuristic]
    for i in range(3,9):
        for j in range(1,4):
            data[i][j] = pd.read_csv(f"Results/res{i}_h{j}.csv")
            #print(f"Depth of {i} has an average time of {sum(list(data[i][j]['time']))/100:.2f} seconds with h{j}.")
            #print(f"With depth of {i} and h{j}, after 5 seconds, its expected to last {merl(list(data[i][j]['time']), 5)} more seconds")
    
    makeLineChart(data, "time", "Average Solve Times For Each Heuristic", "Depth", "Average Time (sec)")
    makeLineChart(data, "numexp", "Average Number Of States Expanded For Each Heuristic", "Depth", "Average Number Of States Expanded")
    makeLineChart(data, "numgen", "Average Number Of States Generated For Each Heuristic", "Depth", "Average Number Of States Generated")
    
    makeHistogram(data, "time", 1, [-1,5], 15, "Time Distribution For h1 With Depth 8", "Time (sec)", "Frequency")
    makeHistogram(data, "time", 2, [-1,5], 15, "Time Distribution For h2 With Depth 8", "Time (sec)", "Frequency")
    makeHistogram(data, "time", 3, [-1,5], 15, "Time Distribution For h3 With Depth 8", "Time (sec)", "Frequency")

    makeHistogram(data, "numexp", 1, [0,9], 15, "Distribution For Number Of Expanded States For h1 With Depth 8", "Number Of Nodes Expanded", "Frequency")
    makeHistogram(data, "numexp", 2, [0,9], 15, "Distribution For Number Of Expanded States For h2 With Depth 8", "Number Of Nodes Expanded", "Frequency")
    makeHistogram(data, "numexp", 3, [0,9], 15, "Distribution For Number Of Expanded States For h3 With Depth 8", "Number Of Nodes Expanded", "Frequency")
    
    makeMERLchart(data, "time", [0,9], True, "MERL Of Time For Depth 8", "Given Time (sec)", "Expected Remaining Time (sec)")
    makeMERLchart(data, "numexp", [0,9], True, "MERL Of Expanded States For Depth 8", "Expanded States So far", "Expected Remaining States")
    makeMERLchart(data, "numgen", [0,9], True, "MERL Of Generated States For Depth 8", "Generated States So far", "Expected Remaining States")
    
    