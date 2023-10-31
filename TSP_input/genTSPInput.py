def createTSPInput(numNode: int, lower: int, upper: int, is_symmetric: str, fname: str):
    """Create an input for TSP

    #### Parameters:
        numNode      (int):  Number of nodes
        lower        (int):  Lower bound for distance
        upper        (int):  Upper bound for distance
        is_symmetric (bool): Default True
        fname        (str):  File name

    #### Returns:
        Create a file containing input for TSP
        line 1: n = Number of nodes
        line 2 -> n + 1: Distance matrix C, elements are seperated by a space.
        C (i, j): Distance / Cost to move from node i to node j
    """
    import random

    # Create non-symmetrical distance matrix
    def createNonSymInputSize(numNode, lower, upper, filename):
        with open(filename, "w") as file:
            file.write(str(numNode) + "\n")
            for row in range(numNode):
                line = ""
                for col in range(numNode):
                    if col == row:
                        line += "0 "
                    else:
                        line += str(random.randint(lower, upper)) + " "
                file.write(line + "\n")

    # Create symmetrical distance matrix
    def createSymmetricInputSize(numNode, lower, upper, filename):
        with open(filename, "w") as file:
            file.write(str(numNode) + "\n")

            dMatrix = [[0 for col in range(numNode)] for row in range(numNode)]
            for row in range(numNode):
                for col in range(numNode):
                    if col > row:
                        dMatrix[row][col] = random.randint(lower, upper)
                    if col < row:
                        dMatrix[row][col] = dMatrix[col][row]

                file.write(" ".join(map(str, dMatrix[row])) + "\n")

    if is_symmetric:
        createSymmetricInputSize(numNode, lower, upper, fname)
    else:
        createNonSymInputSize(numNode, lower, upper, fname)


if __name__ == "__main__":
    numNode = int(input("Number of nodes: "))
    lower = int(input("Lower bound: "))
    upper = int(input("Upper bound: "))
    isSymmetric = input("Symmetric? (Y/N): ").upper()
    filename = input("File name: ")

    if isSymmetric == "Y":
        isSymmetric = True
    elif isSymmetric == "N":
        isSymmetric = False

    createTSPInput(numNode, lower, upper, isSymmetric, filename)
