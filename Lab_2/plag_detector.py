import heapq
import numpy as np

# Function to compute Levenshtein distance between two strings
def calculate_levenshtein(source, target):
    len_source, len_target = len(source), len(target)
    distance_matrix = np.zeros((len_source + 1, len_target + 1), dtype=int)

    for i in range(len_source + 1):
        distance_matrix[i][0] = i
    for j in range(len_target + 1):
        distance_matrix[0][j] = j

    for i in range(1, len_source + 1):
        for j in range(1, len_target + 1):
            if source[i - 1] == target[j - 1]:
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
            else:
                distance_matrix[i][j] = min(distance_matrix[i - 1][j] + 1,
                                             distance_matrix[i][j - 1] + 1,
                                             distance_matrix[i - 1][j - 1] + 1)

    return distance_matrix[len_source][len_target]

# A* search algorithm implementation for aligning two documents
def a_star_text_alignment(document1, document2):
    initial_state = (0, 0, 0)  # (index_in_doc1, index_in_doc2, total_cost)
    final_state = (len(document1), len(document2))
    open_list = [(0, initial_state)]  # (cost, state)

    explored = set()

    while open_list:
        current_cost, current_state = heapq.heappop(open_list)
        index1, index2, total_cost = current_state

        if (index1, index2) in explored:
            continue

        explored.add((index1, index2))

        # Check if the target state has been reached
        if index1 == final_state[0] and index2 == final_state[1]:
            return total_cost

        # Explore possible transitions and their costs
        if index1 < len(document1) and index2 < len(document2):
            new_cost = total_cost + calculate_levenshtein(document1[index1], document2[index2])
            heapq.heappush(open_list, (new_cost, (index1 + 1, index2 + 1, new_cost)))

        # Skip sentence in document1
        if index1 < len(document1):
            new_cost = total_cost + len(document1[index1])  # Maximum cost for skipping
            heapq.heappush(open_list, (new_cost, (index1 + 1, index2, new_cost)))

        # Skip sentence in document2
        if index2 < len(document2):
            new_cost = total_cost + len(document2[index2])  # Maximum cost for skipping
            heapq.heappush(open_list, (new_cost, (index1, index2 + 1, new_cost)))

# Function to preprocess text documents
def tokenize_and_normalize(text):
    sentences = text.split('.')
    return [sentence.strip().lower() for sentence in sentences if sentence.strip()]

# Function to execute and display results for test cases
def execute_test_case(doc_one, doc_two, case_number):
    doc_one_sentences = tokenize_and_normalize(doc_one)
    doc_two_sentences = tokenize_and_normalize(doc_two)

    alignment_cost = a_star_text_alignment(doc_one_sentences, doc_two_sentences)

    print(f"Test Case {case_number}:")
    print(f"Document 1: {doc_one}")
    print(f"Document 2: {doc_two}")
    print(f"Alignment Cost: {alignment_cost}")
    print("\n" + "=" * 40 + "\n")

# Updated Test Cases

# Test Case 1: Identical Texts
doc_one = "Climate change is a pressing issue. It requires global action."
doc_two = "Climate change is a pressing issue. It requires global action."
execute_test_case(doc_one, doc_two, 1)

# Test Case 2: Slightly modified
doc_one = "The economy is showing signs of recovery. Job rates are improving."
doc_two = "The economy is showing signs of improvement. Job rates are increasing."
execute_test_case(doc_one, doc_two, 2)

# Test Case 3: Completely Different Documents
doc_one = "Artificial Intelligence is transforming industries. It is the future."
doc_two = "Gardening is a therapeutic activity. It connects us with nature."
execute_test_case(doc_one, doc_two, 3)

# Test Case 4: Partial Overlap
doc_one = "The solar system consists of various celestial bodies. Each planet has its own characteristics."
doc_two = "The solar system consists of various celestial bodies. Each planet has its own unique features."
execute_test_case(doc_one, doc_two, 4)