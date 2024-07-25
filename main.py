import datetime

import csv
from address import Address
from hash_table import HashTableWithChaining as HashTable
from package import Package

#
# Global variables
#
ADDRESSES = []
PACKAGES = HashTable(10)
DISTANCES = {}


def package_lookup(package_id: int) -> Package:
    return PACKAGES.search(package_id)


def address_lookup(address_id: int) -> Address:
    return ADDRESSES[address_id]


def get_address_by_street(street: str) -> Address or None:
    for addr in ADDRESSES:
        if addr.street == street:
            return addr
    return None


def get_distance(i: int, j: int) -> float:
    return DISTANCES[i, j]


# Convert time string to minutes
# "10:30 AM" -> 10:30 , "10:30 PM"-> 22:30
def convert_time(time_str) -> datetime.timedelta:
    if time_str == 'EOD':
        return datetime.timedelta(hours=23, minutes=59)
    time = time_str.split(':')
    hour = int(time[0])
    minute = int(time[1].split(' ')[0])
    if time[1].split(' ')[1] == 'PM':
        hour += 12
    return datetime.timedelta(hours=hour, minutes=minute)


#
# Load data from CSV files
#
print('Loading addresses...')
with open('csv/addresses.csv', 'r') as address_file:
    address_data = csv.reader(address_file)
    address_data = list(address_data)

# Create a list of Address objects
for address in address_data:
    addr = Address(address[0], address[1], address[2])
    ADDRESSES.insert(addr.ID, addr)

print('Loading packages...')
with open('csv/packages.csv', 'r') as package_file:
    package_data = csv.reader(package_file)
    package_data = list(package_data)

    for package in package_data:
        # 1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21,
        parcel = Package(package[0], package[6], package[7])
        addr = get_address_by_street(package[1])
        addr.street = package[1]
        addr.city = package[2]
        addr.state = package[3]
        addr.zip = package[4]

        ADDRESSES.insert(addr.ID, addr)
        parcel.address = addr
        parcel.deadline = convert_time(package[5])

        PACKAGES.insert(parcel.ID, parcel)

print('Populating distance dictionary...')
with open('csv/distances.csv', 'r') as distance_file:
    distance_data = csv.reader(distance_file)
    distance_data = list(distance_data)

for i in range(len(distance_data)):
    for j in range(len(distance_data[i])):
        if distance_data[i][j] == '':
            DISTANCES[i, j] = 0.0
        else:
            DISTANCES[i, j] = float(distance_data[i][j])


#
# Greedy algorithms/optimization
#

# Nearest neighbor algorithm
# O(n^2) time complexity
# This algorithm is secondary to the 2-opt optimization algorithm and is only used on the 'priority' packages
def nearest_neighbor(start, address_list) -> list:
    print('Calculating nearest neighbor...')
    max_i = len(address_list)
    route = [start]
    visited = [False] * len(address_list)

    while len(route) < max_i:
        current = route[-1]
        nearest = None
        nearest_distance = float('inf')

        for i in range(len(address_list)):
            if not visited[i] and DISTANCES[current, i] < nearest_distance:
                nearest = i
                nearest_distance = DISTANCES[current, i]

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


def sum_route_distance(route) -> float:
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += DISTANCES[route[i], route[i + 1]]
    total_distance += DISTANCES[route[-1], route[0]]
    return total_distance


def two_opt_swap(route, i, k):
    new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route


#
# Main control flow
#


def intro():
    # time.sleep(1)
    print('<- Press Ctrl+C to quit at any time ->')
    #     time.sleep(1)

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


def run_simulation():
    print('Running simulation...')


def user_interface():
    print('User interface...')
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
                print('Lookup packages')
                print(PACKAGES.inspect())
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


#                 time.sleep(1)


def main():
    intro()
    initialize()
    run_simulation()
    user_interface()
    exit()


if __name__ == '__main__':
    main()
