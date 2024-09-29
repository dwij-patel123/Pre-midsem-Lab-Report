import random

def create_k_sat_clause(num_vars, num_clauses, clause_length):
    var_names = [f"y{i}" for i in range(1, num_vars + 1)]
    k_sat_expression = []

    for _ in range(num_clauses):
        current_clause = random.sample(var_names + [f"~{var}" for var in var_names], clause_length)
        k_sat_expression.append("(" + " OR ".join(current_clause) + ")")

    return k_sat_expression

length_of_clause = int(input("Enter the length of each clause: ")) #k
number_of_clauses = int(input("Enter the number of clauses: ")) #m
number_of_variables = int(input("Enter the number of variables: ")) #n

generated_k_sat_expression = create_k_sat_clause(number_of_variables, number_of_clauses, length_of_clause)

print("Generated k-SAT expression:")
print("(" + " AND ".join(generated_k_sat_expression) + ")")
