from collections import deque
import heapq
import random

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g # distance to root
        self.h = h # estimated distance to goal
        self.f = g + h # evaluation function
    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal_state):
    h = 0
    # Manhattan Distance as heuristic
    for i in range(9):
        if node.state[i] != 0:  # Skip the blank tile
            goal_index = goal_state.index(node.state[i])
            current_row, current_col = i // 3, i % 3
            goal_row, goal_col = goal_index // 3, goal_index % 3
            h += abs(current_row - goal_row) + abs(current_col - goal_col)
    return h

def get_successors(node):
    successors = []
    index = node.state.index(0)  # Position of blank tile (0)
    quotient = index // 3
    remainder = index % 3
    moves = []

    # Row constrained moves
    if quotient > 0:
        moves.append(-3)  # Move up
    if quotient < 2:
        moves.append(3)   # Move down
    
    # Column constrained moves
    if remainder > 0:
        moves.append(-1)  # Move left
    if remainder < 2:
        moves.append(1)   # Move right

    for move in moves:
        im = index + move
        if 0 <= im < 9:  # Ensure the move is within bounds
            new_state = list(node.state)
            new_state[index], new_state[im] = new_state[im], new_state[index]
            successor = Node(new_state, node, node.g + 1)
            successors.append(successor)
    return successors

def search_agent(start_state, goal_state):
    start_node = Node(start_state, g=0, h=heuristic(Node(start_state), goal_state))
    frontier = []
    heapq.heappush(frontier, (start_node.f, start_node))
    visited = set()
    visited_states_count = 0  # Counter for visited states

    while frontier:
        _, node = heapq.heappop(frontier)
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        visited_states_count += 1  # Increment counter for visited states

        if node.state == goal_state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print(f"Number of visited states: {visited_states_count}")  # Print visited states count
            return path[::-1]

        for successor in get_successors(node):
            if tuple(successor.state) not in visited:
                successor.h = heuristic(successor, goal_state)
                successor.f = successor.g + successor.h
                heapq.heappush(frontier, (successor.f, successor))

    print(f"Number of visited states: {visited_states_count}")  # Print visited states count if no solution
    return None

# Example start and goal states
start_state = [1, 2, 3, 5, 6, 0, 7, 8, 4]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

solution = search_agent(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
