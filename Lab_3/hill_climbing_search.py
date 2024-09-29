import random
import time

def generate_clauses(num_clauses, num_vars):
    """Generate random 3-SAT clauses."""
    variables = list(range(1, num_vars + 1))
    clauses = []
    for _ in range(num_clauses):
        selected_vars = random.sample(variables, 3)
        clause = [(var, random.choice([True, False])) for var in selected_vars]
        clauses.append(clause)
    return clauses

def random_assignment(num_vars):
    """Create a random truth assignment for the variables."""
    return [random.choice([True, False]) for _ in range(num_vars)]

def count_unsatisfied(clauses, assignment):
    """Count how many clauses are not satisfied by the assignment."""
    return sum(1 for clause in clauses if not evaluate_clause(clause, assignment))

def evaluate_clause(clause, assignment):
    """Evaluate a single clause against a given truth assignment."""
    return any((var > 0 and assignment[var - 1]) or (var < 0 and not assignment[-var - 1]) for var, _ in clause)

def hill_climb(clauses, num_vars, max_iterations=1000):
    """Perform Hill Climbing algorithm to find a satisfying assignment."""
    current_assignment = random_assignment(num_vars)
    unsatisfied_count = count_unsatisfied(clauses, current_assignment)

    for _ in range(max_iterations):
        neighbor = current_assignment.copy()
        flip_index = random.randint(0, num_vars - 1)
        neighbor[flip_index] = not neighbor[flip_index]

        neighbor_count = count_unsatisfied(clauses, neighbor)

        if neighbor_count < unsatisfied_count:
            current_assignment = neighbor
            unsatisfied_count = neighbor_count
            
            if unsatisfied_count == 0:
                return current_assignment  # Solution found

    return None  # No solution found within the max iterations

def main():
    num_clauses = 8
    num_vars = 18
    clauses = generate_clauses(num_clauses, num_vars)

    print(f"Attempting to solve 3-SAT with {num_clauses} clauses and {num_vars} variables using Hill Climbing.")
    print("Generated Clauses:")
    print(clauses)
    
    start_time = time.time()
    solution = hill_climb(clauses, num_vars)
    end_time = time.time()

    print(f"Found Solution: {solution}")
    print(f"Execution Duration: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()
