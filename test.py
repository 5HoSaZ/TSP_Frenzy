from GetTSPInput import getInput
from ortools.sat.python import cp_model

NUM_NODES, DISTANCE_MATRIX = getInput("50_nodes.tsp")


def main():
    """Entry point of the program."""
    num_nodes = NUM_NODES
    all_nodes = range(num_nodes)
    print("Num nodes =", num_nodes)

    # Model.
    model = cp_model.CpModel()

    obj_vars = []
    obj_coeffs = []

    # Create the circuit constraint.
    arcs = []
    arc_literals = {}
    for i in all_nodes:
        for j in all_nodes:
            if i == j:
                continue

            lit = model.NewBoolVar("%i follows %i" % (j, i))
            arcs.append([i, j, lit])
            arc_literals[i, j] = lit

            obj_vars.append(lit)
            obj_coeffs.append(DISTANCE_MATRIX[i][j])

    model.AddCircuit(arcs)

    # Minimize weighted sum of arcs. Because this s
    model.Minimize(sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    # To benefit from the linearization of the circuit constraint.
    solver.parameters.linearization_level = 2

    solver.Solve(model)
    print(solver.ResponseStats())

    current_node = 0
    str_route = "%i" % current_node
    route_is_finished = False
    route_distance = 0
    while not route_is_finished:
        for i in all_nodes:
            if i == current_node:
                continue
            if solver.BooleanValue(arc_literals[current_node, i]):
                str_route += " -> %i" % i
                route_distance += DISTANCE_MATRIX[current_node][i]
                current_node = i
                if current_node == 0:
                    route_is_finished = True
                break

    print("Route:", str_route)
    print("Travelled distance:", route_distance)


if __name__ == "__main__":
    main()
