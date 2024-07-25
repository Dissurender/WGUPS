import datetime
import time

import csv
from address import Address
from hash_table import HashTableWithChaining as HashTable
from package import Package


#
# Load data from CSV files
#
def load_addresses() -> list:
    print('Loading addresses...')
    with open('csv/addresses.csv', 'r') as address_file:
        address_data = csv.reader(address_file)
        address_data = list(address_data)

    address_list = [] * len(address_data)
    for address in address_data:
        addr = Address(address[0], address[1], address[2])
        address_list.append(addr)

    return address_list


def load_packages() -> HashTable:
    print('Loading packages...')
    packages = HashTable(10)
    with open('csv/packages.csv', 'r') as package_file:
        package_data = csv.reader(package_file)
        package_data = list(package_data)

        for package in package_data:
            parcel = Package(package[0], package[1], package[2], package[3], package[4])
            packages.insert(parcel.ID, parcel)

    return packages


def load_distances() -> dict:
    print('Populating distance dictionary...')
    with open('csv/distances.csv', 'r') as distance_file:
        distance_data = csv.reader(distance_file)
        distance_data = list(distance_data)

    # Create a dictionary to store the distances between addresses
    distance_dict = {}
    for i in range(len(distance_data)):
        for j in range(len(distance_data[i])):
            if distance_data[i][j] == '':
                distance_dict[i, j] = 0.0
            else:
                distance_dict[i, j] = float(distance_data[i][j])

    return distance_dict


#
# Helper functions
#

def package_lookup(package_id) -> Package:
    pass


def address_lookup(address_id) -> Address:
    pass


# Convert time string to minutes
def convert_time(time_str) -> datetime.timedelta:
    time = time_str.split(':')
    hours = int(time[0])
    minutes = int(time[1][2:])
    if time[1][:2] == 'PM':
        hours += 12
    return datetime.timedelta(hours=hours, minutes=minutes)


def parse_packages(package_list):
    pass


def parse_addresses(address_list):
    pass


#
# Greedy algorithms/optimization
#

# Nearest neighbor algorithm
# O(n^2) time complexity
# This algorithm is secondary to the 2-opt optimization algorithm and is only used on the 'priority' packages
def nearest_neighbor(start, address_list) -> list:
    print('Calculating nearest neighbor...')
    distances = main.distance_dict
    max_i = len(address_list)
    route = [start]
    visited = [False] * len(address_list)

    while len(route) < max_i:
        current = route[-1]
        nearest = None
        nearest_distance = float('inf')

        for i in range(len(address_list)):
            if not visited[i] and distances[current, i] < nearest_distance:
                nearest = i
                nearest_distance = distances[current, i]

        route.append(nearest)
        visited[nearest] = True

    return route


# 2-opt optimization algorithm
# This algorithm is used to optimize the 'standard' packages route for shortest distance
# O(N^3) time complexity
def two_opt(route) -> tuple[list, float]:
    print('Optimizing route with 2-opt...')
    best_route = route
    improved = True
    best_distance = 0.0

    while improved:
        improved = False
        best_distance = sum_route_distance(best_route)

        for i in range(1, len(best_route) - 1):
            for j in range(i + 1, len(best_route) - 1):
                new_route = two_opt_swap(best_route, i, j)
                new_distance = sum_route_distance(new_route)

                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
    return best_route, best_distance


def sum_route_distance(route):
    distances = main.distance_dict
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += distances[route[i], route[i + 1]]
    total_distance += distances[route[-1], route[0]]
    return total_distance


def two_opt_swap(route, i, k):
    new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route


#
# Main control flow
#


def intro():
    time.sleep(1)
    print('<- Press Ctrl+C to quit at any time ->')
    time.sleep(1)

    print("""
            _____________________________________________
           /  __          _______ _    _ _____   _____   \\
           |  \ \        / / ____| |  | |  __ \ / ____|  |\\\\\\\\\\\\
           |   \ \  /\  / / |  __| |  | | |__) | (___    |------
           |    \ \/  \/ /| | |_ | |  | |  ___/ \___ \\   |\\\\\\\\\\\\\\\\
           |     \  /\  / | |__| | |__| | |     ____) |  |--------
           |      \/  \/   \_____|\____/|_|    |_____/   |\\\\\\\\\\\\\\\\\\\\
            \\___________________________________________/
            """)
    print('Starting Service...')


def initialize():
    print('Initializing...')
    time.sleep(1)


def run_simulation():
    print('Running simulation...')
    time.sleep(1)


def user_interface():
    print('User interface...')
    time.sleep(1)
    menu = """
            Welcome to the WGUPS package tracking system!
            Please select an option:
            1. Lookup package
            2. Lookup address
            3. Print all packages
            4. Print all addresses
            5. Exit
            
            6. Show menu
            """

    while True:
        user_input = input(menu + '\nEnter choice: ')

        match user_input:
            case '1':
                print('Lookup package')
            case '2':
                print('Lookup address')
            case '3':
                print('Print all packages')
            case '4':
                print('Print all addresses')
            case '5':
                print('Exiting...')
                break
            case '6':
                print(menu)
            case _:
                print('\nInvalid input. Please select and option by its #.')
                time.sleep(1)


# Main class to hold state and control flow
class Main:
    def __init__(self):
        self.package_list = load_packages()
        self.address_list = load_addresses()
        self.distance_dict = load_distances()

    def run(self):
        intro()
        initialize()
        run_simulation()
        user_interface()
        exit()


if __name__ == '__main__':
    main = Main()
    main.run()
