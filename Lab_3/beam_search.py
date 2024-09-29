import random

def create_random_3sat(num_clauses, num_vars):
    """Generate random 3-SAT clauses."""
    var_range = range(1, num_vars + 1)
    clauses_list = []
    for _ in range(num_clauses):
        selected_clause = random.sample(var_range, 3)
        clause = [(var, random.choice([True, False])) for var in selected_clause]
        clauses_list.append(clause)
    return clauses_list

def create_random_assignment(num_vars):
    """Generate a random assignment of truth values."""
    return [random.choice([True, False]) for _ in range(num_vars)]

def count_unsatisfied(clauses, assignment):
    """Count the number of unsatisfied clauses for a given assignment."""
    unsatisfied_count = 0
    for clause in clauses:
        clause_evaluation = any((var > 0 and assignment[var - 1]) or (var < 0 and not assignment[-var - 1]) for var, _ in clause)
        if not clause_evaluation:
            unsatisfied_count += 1
    return unsatisfied_count

def beam_search_solver(clauses, num_vars, beam_width):
    """Perform Beam Search to solve the 3-SAT problem."""
    current_beam = [create_random_assignment(num_vars) for _ in range(beam_width)]

    for _ in range(1000):  # Maximum iterations
        next_candidates = []

        for assignment in current_beam:
            for index in range(num_vars):
                temp_assignment = assignment.copy()
                temp_assignment[index] = not temp_assignment[index]

                if count_unsatisfied(clauses, temp_assignment) == 0:
                    return temp_assignment  # Solution found

                next_candidates.append(temp_assignment)

        # Sort candidates by the number of unsatisfied clauses
        next_candidates.sort(key=lambda x: count_unsatisfied(clauses, x))
        current_beam = next_candidates[:beam_width]

    return None  # No solution found within the iteration limit

def main():
    num_clauses = 10
    num_vars = 20
    clauses = create_random_3sat(num_clauses, num_vars)
    print("Generated Clauses:")
    print(clauses)

    print(f"\nAttempting to solve 3-SAT with {num_clauses} clauses and {num_vars} variables using Beam Search (beam width = 3)")
    solution = beam_search_solver(clauses, num_vars, beam_width=3)
    print(f"Found Solution: {solution}")

    print(f"\nAttempting to solve 3-SAT with {num_clauses} clauses and {num_vars} variables using Beam Search (beam width = 4)")
    solution = beam_search_solver(clauses, num_vars, beam_width=4)
    print(f"Found Solution: {solution}")

if __name__ == "__main__":
    main()
