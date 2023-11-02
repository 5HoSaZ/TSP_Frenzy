from heapq import heappush, heappop
from TSP_Input.GetTSPInput import getInput

# For TSP problem, we have the number of nodes and the distance matrix

NUM_NODES, PATH_COST = getInput("10.tsp")
INF = float("inf")
NODES = set(range(NUM_NODES))
ROOT_POS = 0

# Goal: find the minimum distance path that traversed through all nodes


# Use a priority queue to perform Branch and Bound
class PriorityQueue:
    def __init__(self):
        self.heap = []

    # Inserts a new key 'k'
    def push(self, k):
        heappush(self.heap, k)

    # remove minimum element
    def pop(self):
        return heappop(self.heap)

    # Check if queue is empty
    def empty(self):
        if not self.heap:
            return True
        else:
            return False


class Node:
    def __init__(self, level, parent, pos, to_traverse, path, distance):
        # Heap level
        self.level = level

        # Node's parent
        self.parent = parent

        # Current position
        self.pos = pos

        # Nodes to travers
        self.to_traverse = to_traverse

        # Lower bound
        self.lb = lb(self)

        # Path traveled so far
        self.path = path

        # Distance traveled so far
        self.distance = distance

    # The goal is to find the minimum travel distance
    def __lt__(self, nxt):
        return self.distance < nxt.distance

    def __str__(self):
        string = (
            f"level: {self.level}\n"
            + f"path {self.path}\nto traverse {self.to_traverse}\n"
            + f"lb: {self.lb}\n"
            + f"d: {self.distance}"
        )
        return string


class RootNode(Node):
    def __init__(self, root_pos):
        super().__init__(0, None, root_pos, NODES - {root_pos}, [root_pos], root_pos)


def minPathFrom(cur_pos):
    min = INF
    for nxt_pos in NODES - {cur_pos}:
        if PATH_COST[cur_pos][nxt_pos] < min:
            min = PATH_COST[cur_pos][nxt_pos]
    return min


def minPathTo(cur_pos):
    min = INF
    for prv_pos in NODES - {cur_pos}:
        if PATH_COST[prv_pos][cur_pos] < min:
            min = PATH_COST[prv_pos][cur_pos]
    return min


def lb(node: Node):
    if node.parent is None:
        return sum([(minPathFrom(i) + minPathTo(i)) / 2 for i in NODES])

    i = node.parent.pos
    j = node.pos
    return node.parent.lb - (minPathFrom(i) + minPathTo(j)) / 2 + PATH_COST[i][j]


def nextNode(cur_node: Node, nxt_pos) -> Node:
    return Node(
        level=cur_node.level + 1,
        parent=cur_node,
        pos=nxt_pos,
        to_traverse=cur_node.to_traverse - {nxt_pos},
        path=cur_node.path[:] + [nxt_pos],
        distance=cur_node.distance + PATH_COST[cur_node.pos][nxt_pos],
    )


def printSolution(Node):
    print("Optimal objective value ==", Node.distance)
    print("Optimal path:", end=" ")
    print(*map(lambda x: x + 1, Node.path), sep=" -> ")


def mainTSP():
    pq = PriorityQueue()

    # Root node
    rootNode = RootNode(ROOT_POS)
    best = INF
    sol = 0
    pq.push(rootNode)

    while not pq.empty():
        minimum = pq.pop()
        if minimum.level == NUM_NODES:
            if minimum.lb <= best:
                best = minimum.lb
                sol = minimum
        elif minimum.lb <= best:
            if minimum.to_traverse:
                for nxt_pos in minimum.to_traverse:
                    nxtNode = nextNode(minimum, nxt_pos)
                    pq.push(nxtNode)
            elif minimum.level == NUM_NODES - 1:
                nxtNode = nextNode(minimum, ROOT_POS)
                pq.push(nxtNode)
    printSolution(sol)
    # printSolution(sol)


if __name__ == "__main__":
    mainTSP()
