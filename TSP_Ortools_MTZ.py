import logging as log
from ortools.linear_solver import pywraplp
from TSP_Input.GetTSPInput import getInput
from time import time

# Setting up logger
for handler in log.root.handlers[:]:
    log.root.removeHandler(handler)
log.basicConfig(format="%(levelname)s - %(message)s")

logger = log.getLogger()
logger.setLevel(log.DEBUG)
log.info("Logger initialized...")


# Print solution
def printSolutionFromX(X, numNode):
    start = 0
    print(start + 1, end=" ")
    for step in range(numNode - 1):
        for end in range(numNode):
            if X[(start, end)].solution_value() == 1:
                print("->", end + 1, end=" ")
                start = end
                break
    print("->", 1)


def printSolutionFromU(U, numNode):
    path = sorted((U[i].solution_value(), i + 1) for i in range(numNode))
    print("Optimal tour: ", end="")
    print(*[path[step][1] for step in range(numNode)], 1, sep=" -> ")


def TSPMain(numNode, pathCost):
    solver_id = "SCIP"
    solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(solver_id)

    log.info("Creating " + str(numNode * numNode) + " boolean x_ij variables... ")
    X = {}
    for i in range(numNode):
        for j in range(numNode):
            X[(i, j)] = solver.BoolVar(f"x{(i, j)}")

    # Constraint 1: Leave every node exactly once
    log.info("Creating " + str(numNode - 1) + " Constraint 1... ")
    for i in range(numNode):
        solver.Add(sum(X[(i, j)] for j in range(numNode) if j != i) == 1)

    # Constraint 2: Reach every node from exactly one other node
    log.info("Creating " + str(numNode - 1) + " Constraint 2... ")
    for j in range(numNode):
        solver.Add(sum(X[(i, j)] for i in range(numNode) if i != j) == 1)

    # Constraint 3: MTZ subtour elimination constraints (Miller-Tucker-Zemlin)
    U = {}
    U[0] = solver.IntVar(1, 1, "u0")
    for i in range(1, numNode):
        U[i] = solver.IntVar(2, numNode, f"u{i}")

    log.info("Creating " + str((numNode - 1) ** 2) + " MTZ Constraint ... ")
    for i in range(1, numNode):
        for j in range(1, numNode):
            solver.Add(U[i] - U[j] + 1 <= (numNode - 1) * (1 - X[(i, j)]))

    # Objective function
    solver.Minimize(
        sum(X[(i, j)] * pathCost[i][j] for i in range(numNode) for j in range(numNode))
    )
    log.info("Solving model... ")

    # Solve TSP
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal objective value ==", solver.Objective().Value())
        # printSolutionFromX(X, numNode)
        printSolutionFromU(U, numNode)
    else:
        print("UNBOUNDED")


if __name__ == "__main__":
    start = time()
    numNode, PathCost = getInput("10.tsp")
    TSPMain(numNode, PathCost)
    end = time()
    print(f"Execution time: {end-start}")
