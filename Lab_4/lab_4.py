from math import radians, sin, cos, sqrt, atan2
import random
import math

# Tourist locations in Rajasthan
locations = [
    "Jaipur", "Udaipur", "Jodhpur", "Jaisalmer", "Ajmer", "Pushkar",
    "Mount Abu", "Ranthambore National Park", "Bikaner", "Chittorgarh",
    "Sawai Madhopur", "Alwar", "Bharatpur Bird Sanctuary", "Kumbhalgarh Fort",
    "Mehrangarh Fort", "Hawa Mahal", "City Palace, Jaipur", "Amber Palace",
    "Junagarh Fort", "Sheesh Mahal, Udaipur",
]


def calc_distance(loc1, loc2):
    coords = {
        "Jaipur": (26.9124, 75.7873), "Udaipur": (24.5854, 73.7125), "Jodhpur": (26.2389, 73.0243),
        "Jaisalmer": (26.9157, 70.9083), "Ajmer": (26.4499, 74.6399), "Pushkar": (26.4896, 74.5511),
        "Mount Abu": (24.5928, 72.7156), "Ranthambore National Park": (25.9928, 76.3677),
        "Bikaner": (28.0229, 73.3119), "Chittorgarh": (24.8887, 74.6269),
        "Sawai Madhopur": (25.9870, 76.5527), "Alwar": (27.5530, 76.6346),
        "Bharatpur Bird Sanctuary": (27.1751, 77.5044), "Kumbhalgarh Fort": (25.1484, 73.5877),
        "Mehrangarh Fort": (26.2979, 73.0187), "Hawa Mahal": (26.9239, 75.8267),
        "City Palace, Jaipur": (26.9258, 75.8236), "Amber Palace": (26.9855, 75.8513),
        "Junagarh Fort": (28.0189, 73.3197), "Sheesh Mahal, Udaipur": (24.5854, 73.7125)
    }
    lat1, lon1 = coords[loc1]
    lat2, lon2 = coords[loc2]
    d_lon, d_lat = lon2 - lon1, lat2 - lat1
    return sqrt(d_lon ** 2 + d_lat ** 2)


def total_route_distance(route):
    total = sum(calc_distance(route[i], route[i + 1]) for i in range(len(route) - 1))
    total += calc_distance(route[-1], route[0])
    return total


def annealing_algorithm(locations, num_iter, temp_init, cool_rate):
    current_route = locations[:]
    best_route = locations[:]
    temp = temp_init

    for _ in range(num_iter):
        new_route = current_route[:]
        idx1, idx2 = random.sample(range(len(new_route)), 2)
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]

        current_cost = total_route_distance(current_route)
        new_cost = total_route_distance(new_route)

        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temp):
            current_route = new_route[:]

        if total_route_distance(current_route) < total_route_distance(best_route):
            best_route = current_route[:]

        temp *= 1 - cool_rate

    return best_route


iterations = 10000
initial_temperature = 1000.0
cooling_rate = 0.003

best_route = annealing_algorithm(locations, iterations, initial_temperature, cooling_rate)
print("Optimal route:", best_route)
print("Total route distance:", total_route_distance(best_route))


def parse_tsplib_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        coord_section = False
        coords = []
        for line in lines:
            if line.startswith('NODE_COORD_SECTION'):
                coord_section = True
                continue
            if line.startswith('EOF'):
                break
            if coord_section:
                data = line.strip().split()
                coords.append((float(data[1]), float(data[2])))
        return coords


def euclidean_dist(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def total_tour_dist(tour, nodes):
    total = sum(euclidean_dist(nodes[tour[i]], nodes[tour[i + 1]]) for i in range(len(tour) - 1))
    total += euclidean_dist(nodes[tour[-1]], nodes[tour[0]])
    return total


def tsp_annealing(nodes, num_iter, temp_init, cool_rate):
    n = len(nodes)
    curr_tour = list(range(n))
    random.shuffle(curr_tour)
    best_tour = curr_tour[:]
    temp = temp_init

    for _ in range(num_iter):
        curr_cost = total_tour_dist(curr_tour, nodes)

        new_tour = curr_tour[:]
        start, end = sorted(random.sample(range(n), 2))
        new_tour[start:end] = reversed(new_tour[start:end])
        new_cost = total_tour_dist(new_tour, nodes)

        if new_cost < curr_cost or random.random() < math.exp((curr_cost - new_cost) / temp):
            curr_tour = new_tour[:]

        if total_tour_dist(curr_tour, nodes) < total_tour_dist(best_tour, nodes):
            best_tour = curr_tour[:]

        temp *= 1 - cool_rate

    return best_tour


filename = "xqg237.tsp"
nodes = parse_tsplib_file(filename)

iterations = 100000
initial_temperature = 1000.0
cooling_rate = 0.0003

optimal_tour = tsp_annealing(nodes, iterations, initial_temperature, cooling_rate)
print("Optimal tour:", optimal_tour)
print("Total distance (km):", total_tour_dist(optimal_tour, nodes))

import matplotlib.pyplot as plt


def display_tour(nodes, tour):
    x_vals = [node[0] for node in nodes]
    y_vals = [node[1] for node in nodes]
    # define figure size
    plt.figure(figsize=(8, 6))
    plt.scatter(x_vals, y_vals, color='blue')
    plt.title('TSP Solution xqg237')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    for i in range(len(tour) - 1):
        plt.plot([nodes[tour[i]][0], nodes[tour[i + 1]][0]], [nodes[tour[i]][1], nodes[tour[i + 1]][1]], color='red')


    plt.plot([nodes[tour[-1]][0], nodes[tour[0]][0]], [nodes[tour[-1]][1], nodes[tour[0]][1]], color='red')
    plt.show()


display_tour(nodes, optimal_tour)
