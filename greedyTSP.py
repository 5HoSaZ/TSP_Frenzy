import numpy as np


def getInput(file):
    with open(file, "r") as data:
        numNode = int(next(data))
        distance_matrix = np.loadtxt(data, dtype="int")

    return numNode, distance_matrix


def GreedyTSP(numNode, distance_matrix, start_node=0):
    Nodes = set(range(numNode))
    PCost = distance_matrix

    curr = start_node
    result = 0

    while Nodes:
        Nodes.remove(curr)
        minNext = start_node
        minPath = 1e8
        for next in Nodes:
            if PCost[curr, next] < minPath:
                minNext = next
                minPath = PCost[curr, next]
        result += PCost[curr, minNext]
        print(f"{curr} -> {minNext}: {PCost[curr, minNext]}")
        curr = minNext

    return result


if __name__ == "__main__":
    print(GreedyTSP(*getInput("largeTSP.txt")))
