from collections import deque

def get_blank_position(state):
    # Find the position of the blank tile (0)
    index = state.index(0)
    return index // 3, index % 3

def is_valid(position):
    i, j = position
    return (0 <= i < 3) and (0 <= j < 3)

def get_successors(state):
    successors = []
    i, j = get_blank_position(state)
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    for move in moves:
        new_i, new_j = i + move[0], j + move[1]
        
        if is_valid((new_i, new_j)):
            # Create a copy of the state
            new_state = state[:]
            
            # Swap the blank tile with the tile at the new position
            new_index = new_i * 3 + new_j
            new_state[i * 3 + j], new_state[new_index] = new_state[new_index], new_state[i * 3 + j]
            
            successors.append(new_state)
    
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    
    while queue:
        (state, path) = queue.popleft()
        
        if tuple(state) in visited:
            continue
        
        visited.add(tuple(state))
        path = path + [state]
        
        if state == goal_state:
            print(len(visited))
            return path
        
        for successor in get_successors(state):
            queue.append((successor, path))
    
    return None

# Example usage
start_state = [1, 2, 3, 5, 6, 0, 7, 8, 4] 
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0] 

solution = bfs(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
