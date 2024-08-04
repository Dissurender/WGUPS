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


def truck_assigner(package) -> int:
    id = int(package.ID)
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

    # split packages into priority and standard lists
    for package in packages:
        if package.is_priority:
            priority.append(package)
        else:
            standard.append(package)

    # assign priority packages to trucks 1 and 2
    for package in priority:
        truck = truck_assigner(package)
        if truck is None:
            truck = random.randint(1, 2)
        if truck == 1:
            truck1.priority_packages.append(package)
        elif truck == 2:
            truck2.priority_packages.append(package)

    # assign standard packages to trucks with limited capacity of 16
    for package in standard:
        truck = truck_assigner(package)
        if truck == 1 or (len(truck1.packages) + len(truck1.priority_packages)) < 14:
            truck1.packages.append(package)
        elif truck == 2 or (len(truck2.packages) + len(truck2.priority_packages)) < 14:
            truck2.packages.append(package)
        elif truck == 3 or (len(truck3.packages) + len(truck3.priority_packages)) < 14:
            truck3.packages.append(package)

    print(str(truck1))
    print(str(truck2))
    print(str(truck3))


def user_interface():
    print('User interface...')
    menu = """
            Welcome to the WGUPS package tracking system!
            Please select an option:
            1. Lookup package by ID
            2. Lookup address
            3. Print all packages
            4. Print all addresses
            5. Exit
            
            """

    while True:
        user_input = input(menu + '\nEnter choice: ')

        match user_input:
            case '1':
                print('Lookup package')
                print('Enter package ID: ')
                package_id = input()
                package = PACKAGES.search(package_id)
                print('\nPackage found\n')
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
            case _:
                print('\nInvalid input. Please select and option by its #.')


def main():
    intro()  # Display intro message
    run_simulation()  # Run simulation
    user_interface()  # User Input Loop
    exit()  # Graceful exit


if __name__ == '__main__':
    main()
