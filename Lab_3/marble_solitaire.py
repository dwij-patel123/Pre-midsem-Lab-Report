import time

class Node:
    def __init__(self, state=None, parent=None, path_cost=0):
        self.state = state if state is not None else [[2, 2, 1, 1, 1, 2, 2],
                                                     [2, 2, 1, 1, 1, 2, 2],
                                                     [1, 1, 1, 1, 1, 1, 1],
                                                     [1, 1, 1, 0, 1, 1, 1],
                                                     [1, 1, 1, 1, 1, 1, 1],
                                                     [2, 2, 1, 1, 1, 2, 2],
                                                     [2, 2, 1, 1, 1, 2, 2]]
        self.parent = parent
        self.action = None
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

goal_state = [[2, 2, 0, 0, 0, 2, 2],
              [2, 2, 0, 0, 0, 2, 2],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [2, 2, 0, 0, 0, 2, 2],
              [2, 2, 0, 0, 0, 2, 2]]

total_nodes_expanded = 0

def is_goal_state(state):
    return state == goal_state

def generate_successors(node):
    successors = []
    directions = [(0, -2), (0, 2), (2, 0), (-2, 0)]  # NSEW moves
    step_moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    for i in range(7):
        for j in range(7):
            if node.state[i][j] == 1:
                for k in range(4):
                    c2i, c2j = i + directions[k][0], j + directions[k][1]
                    c1i, c1j = i + step_moves[k][0], j + step_moves[k][1]

                    if is_valid_move(c2i, c2j) and node.state[c1i][c1j] == 1:
                        new_state = [row.copy() for row in node.state]
                        new_node = Node(new_state, node, node.path_cost + 1)

                        new_node.state[c2i][c2j] = 1
                        new_node.state[c1i][c1j] = 0
                        new_node.state[i][j] = 0
                        new_node.action = [[i, j], [c2i, c2j]]
                        successors.append(new_node)

                        global total_nodes_expanded
                        total_nodes_expanded += 1
    return successors

def is_valid_move(x, y):
    return 0 <= x < 7 and 0 <= y < 7

def display_board(state):
    for row in state:
        print(row)

def best_first_search():
    start_node = Node()
    frontier = [start_node]
    explored = set()

    while frontier:
        current_node = frontier.pop()

        display_board(current_node.state)
        print("Path cost: ", current_node.path_cost, "\n")

        if tuple(map(tuple, current_node.state)) in explored:
            continue
        if is_goal_state(current_node.state):
            print("Search ended")
            print("Total nodes explored: ", len(explored))
            return current_node

        explored.add(tuple(map(tuple, current_node.state)))
        children = generate_successors(current_node)
        
        for child in children:
            if tuple(map(tuple, child.state)) not in explored:
                frontier.append(child)

def extract_actions(goal_node):
    actions = []
    while goal_node.parent is not None:
        actions.append(goal_node.action)
        goal_node = goal_node.parent
    return actions[::-1]  # Reverse to get the correct order

if __name__ == "__main__":
    print("Search started")
    start_time = time.time()
    result_node = best_first_search()
    end_time = time.time()

    print("Total nodes expanded: ", total_nodes_expanded)
    print("Time taken: ", end_time - start_time)
    print()
    display_board(result_node.state)

    print("\nMoves: ")
    moves = extract_actions(result_node)
    for move in moves:
        print(move)
