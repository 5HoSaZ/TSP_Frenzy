def getInput(fname):
    """Get TSP input from file.

    #### Parameters:
    fname    (str)     : File name

    #### Returns:
    numNode  (int)     : Number of nodes (n)
    pathCost (NDARRAY) : Distance matrix of (n x n)
    """
    import numpy as np

    with open(fname) as data:
        numNode = int(next(data))
        pathCost = np.loadtxt(data, dtype="int")
    return numNode, pathCost


if __name__ == "__main__":
    numNode, pathCost = getInput("example.tsp")
    print(numNode)
    print(pathCost)
