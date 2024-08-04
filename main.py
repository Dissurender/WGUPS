import datetime
import random

import csv
from address import Address
from hash_table import HashTableWithChaining as HashTable
from package import Package
from truck import Truck

#
# Global state
#
ADDRESSES = []
PACKAGES = HashTable(10)
DISTANCES = {}


# Convert time string to minutes
# "10:30 AM" -> 10:30 , "10:30 PM"-> 22:30
def convert_time(time_str) -> datetime.timedelta:
    if time_str == 'EOD':
        return datetime.timedelta(hours=22, minutes=0)
    time = time_str.split(':')
    hour = int(time[0])
    minute = int(time[1].split(' ')[0])
    if time[1].split(' ')[1] == 'PM':
        hour += 12
    return datetime.timedelta(hours=hour, minutes=minute)


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

    for address in ADDRESSES:
        if address.street == package[1]:
            address.street = package[1]
            address.city = package[2]
            address.state = package[3]
            address.zip = package[4]
            parcel.address = address
            break

    parcel.deadline = convert_time(package[5])

    if parcel.deadline <= datetime.timedelta(hours=10, minutes=30):
        parcel.is_priority = True

    # Insert package into hash table with package ID as key and package data as value
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


def get_address_by_street(address_list, street: str) -> Address or None:
    for addr in address_list:
        if addr.street == street:
            return addr
    return None


def get_distance(distances, i: int, j: int) -> float:
    if distances[i, j]:
        return distances[i, j]
    else:
        return distances[j, i]


def truck_assigner(package):
    id = package.ID
    # handle packages with restrictions
    # must be on truck 2
    if id in [3, 18, 36, 38]:
        return 2
    # delayed packages
    if id in [6, 25, 28, 32]:
        return 1

    # packages that must be delivered together
    if id in [13, 14, 15, 16, 19, 20]:
        return 2

    # packages that must be on truck 3
    if id == 9:
        return 3


#
# Greedy algorithms/optimization
#

# Nearest neighbor algorithm
# O(N^2) time complexity
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
            if not visited[i] and get_distance(DISTANCES, current, i) < nearest_distance:
                nearest = i
                nearest_distance = get_distance(DISTANCES, current, i)

        route.append(nearest)
        visited[nearest] = True

    return route


#
# Main control flow
#


def intro():
    print('<- Press Ctrl+C to quit at any time ->')
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


def run_simulation():
    print('Running simulation...')
    # create trucks
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    # load priority packages
    packages = [PACKAGES.search(i) for i in range(1, 41)]
    priority = []
    standard = []

    # optimize routes
    final_packages = [[], [], []]
    final_route = [[], [], []]

    for i in range(10):
        random.shuffle(standard)
        package_list = [[], [], []]

        # randomly assign packages from standard list to packages 1, 2, and 3
        for j in range(len(standard)):
            if j % 3 == 0:
                package_list[0].append(standard[j])
            elif j % 3 == 1:
                package_list[1].append(standard[j])
            else:
                package_list[2].append(standard[j])

        # collate delivery routes
        delivery_route_1 = [[0, *truck1.priority_packages, *package_list[0], 0], 0.0]
        delivery_route_2 = [[0, *truck2.priority_packages, *package_list[1], 0], 0.0]
        delivery_route_3 = [[0, *truck3.priority_packages, *package_list[2], 0], 0.0]
        delivery_routes = [delivery_route_1, delivery_route_2, delivery_route_3]

        # optimize routes

        # clear package lists
        package_list = [[], [], []]

    # assign package delivery times
    truck1.route = final_route[0]
    truck1.total_distance = final_route[0]
    truck1.packages = final_packages[0]

    truck2.route = final_route[1]
    truck2.total_distance = final_route[1]
    truck2.packages = final_packages[1]

    truck3.route = final_route[2]
    truck3.total_distance = final_route[2]
    truck3.packages = final_packages[2]


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
                print('Lookup package')
                print('Enter package ID: ')
                package_id = input()
                package = PACKAGES.search(package_id)
                print('Package found')
                print(package)
            case '2':
                print('Lookup address')
            case '3':
                print('Lookup packages')
                print(PACKAGES.inspect())
            case '4':
                print('Print all addresses')
            case '5':
                print('Exiting...')
                break
            case '6':
                print(menu)
            case _:
                print('\nInvalid input. Please select and option by its #.')


def main():
    intro()  # Display intro message
    run_simulation()  # Run simulation
    user_interface()  # User Input Loop
    exit()  # Graceful exit


if __name__ == '__main__':
    main()
