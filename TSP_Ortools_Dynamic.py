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
# logger.disabled = True
log.info("Logger initialized...")


# Detect subtours from current solution
def subTourDetector(X):
    path = {
        start: end
        for start in range(numNode)
        for end in range(numNode)
        if X[(start, end)].solution_value() == 1
    }
    Nodes = set(range(numNode))
    subTours = [[]]
    start = 0
    numSubTour = 1
    while True:
        Nodes.remove(start)
        subTours[-1].append((start, path[start]))
        # Traverse every nodes
        if Nodes:
            if path[start] in Nodes:
                start = path[start]
            else:
                start = next(iter(Nodes))
                subTours.append([])
                numSubTour += 1
        else:
            break
    return numSubTour, subTours


# Adding constraints to remove subtours
def removeSubTours(solver, X, subTours):
    for tour in subTours:
        log.info("Removing subtour")
        solver.Add(sum(X[start_end] for start_end in tour) <= len(tour) - 1)
    # log.info("Removing subtour")
    # tour = subTours[0]
    # solver.Add(sum(X[start_end] for start_end in tour) <= len(tour) - 1)


# Print solution
def printSolution(tour):
    start = 0
    print("Optimal tour:", start + 1, end=" ")
    for start, end in tour:
        print("->", end + 1, end=" ")
    print()


# Solver
def TSPMain(numNode, pathCost):
    solver_id = "SCIP"
    solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(solver_id)
    # inf = solver.infinity()

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

    # Create objective function
    solver.Minimize(
        sum(X[(i, j)] * pathCost[i][j] for i in range(numNode) for j in range(numNode))
    )
    log.info("Solving model... ")

    # Dynamically removing subtours until there is only the main tour
    while True:
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            numSubTour, subTours = subTourDetector(X)
            if numSubTour == 1:
                print("Optimal objective value ==", solver.Objective().Value())
                printSolution(subTours[0])
                break
            else:
                removeSubTours(solver, X, subTours)
        else:
            print("UNBOUNDED")
            break


if __name__ == "__main__":
    start = time()
    numNode, pathCost = getInput("50.tsp")
    TSPMain(numNode, pathCost)
    end = time()
    print(f"Execution time: {end-start}")
