# Code by Tran Huu Dao 20220061.

from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    # print intermediate solution
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print("%s = %i" % (v, self.Value(v)), end=" ")
        print()

    def solution_count(self):
        return self.__solution_count


def read_inp():
    n = int(input())
    A = []
    for i in range(n):
        A.append(list(map(int, input().split())))
    B = [[0 for i in range(n + 1)] for j in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            B[i][j] = A[i - 1][j - 1]
    for i in range(2, n + 1):
        B[0][i] = B[1][i]
        B[i][0] = B[i][1]
    return n, B


n, B = read_inp()
# W = sum(sum(row) for row in B)
model = cp_model.CpModel()

# state constraint

# x = [None for i in range(n + 1)]
# for i in range(1, n + 1):
#     x[i] = model.NewIntVar(0, n,'x[' + str(i) + ']')
x = [1 for i in range(n + 1)]
for i in range(1, n + 1):
    x[i] = model.NewIntVar(0, n, "x[{}]".format(i))

W = 0
for i in range(n):
    W += max(B[i])


y = [model.NewIntVar(0, W, "y[{}]".format(i)) for i in range(n + 1)]
# for i in range(n + 1):
#     y[i] = model.NewIntVar(0, W,'y[' + str(i) + ']')

for i in range(1, n + 1):
    model.Add(x[i] != i)
    model.Add(x[i] != 1)

model.Add(x[1] != 0)
for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        model.Add(x[i] != x[j])

# constraints SEC
for i in range(1, n + 1):
    # model.Add(y[x[i]] - y[i] == B[i][x[i]])

    for j in range(n + 1):
        b = model.NewBoolVar(
            "b"
        )  # Thêm logic cstr là 4 dòng này phải dính liền với nhau.
        model.Add(x[i] == j).OnlyEnforceIf(b)
        model.Add(x[i] != j).OnlyEnforceIf(b.Not())
        model.Add(y[j] == y[i] + B[i][j]).OnlyEnforceIf(b)
model.Add(y[1] == 0)
# objective
model.Minimize(y[0])


solver = cp_model.CpSolver()
solver.parameters.search_branching = cp_model.FIXED_SEARCH

vars = [x[i] for i in range(0, n + 1)]

solution_printer = VarArraySolutionPrinter(vars)
solver.Solve(model, solution_printer)

print(solver.Value(y[0]))
