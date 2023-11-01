# Get input from file
def getInput(file):
    import numpy as np

    with open(file) as data:
        numNode = int(next(data))
        pathCost = np.loadtxt(data)
    return numNode, pathCost
