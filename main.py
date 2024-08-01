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
            if not visited[i] and DISTANCES[current, i] < nearest_distance:
                nearest = i
                nearest_distance = DISTANCES[current, i]

        route.append(nearest)
        visited[nearest] = True

    return route


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
    # create trucks
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    # load priority packages
    priority_one = []
    priority_two = []
    priority_three = []

    standard = []

    for i in range(1, 41):
        package = package_lookup(i)

        # handle packages with restrictions
        # must be on truck 2
        if i in [3, 18, 36, 38]:
            priority_two.append(package)

        # delayed packages
        if i in [6, 25, 28, 32]:
            priority_one.append(package)

        # packages that must be delivered together
        if i in [13, 14, 15, 16, 19, 20]:
            priority_two.append(package)

        # packages that must be on truck 3
        if i == 9:
            priority_three.append(package)

        if package.is_priority:
            if package.deadline < convert_time('10:30'):
                priority_two.append(package)
            else:
                priority_one.append(package)
        else:
            standard.append(i)

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

        # get address lists
        address_list_1 = [package_lookup(i).address.ID for i in package_list[0]]
        address_list_2 = [package_lookup(i).address.ID for i in package_list[1]]
        address_list_3 = [package_lookup(i).address.ID for i in package_list[2]]

        # nearest neighbor algorithm
        standard_route_1 = nearest_neighbor(priority_one[-1].address.ID, address_list_1)
        standard_route_2 = nearest_neighbor(priority_two[-1].address.ID, address_list_2)
        standard_route_3 = nearest_neighbor(priority_three[-1].address.ID, address_list_3)

        # collate delivery routes
        delivery_route_1 = [[0, *priority_one, *standard_route_1, 0], 0.0]
        delivery_route_2 = [[0, *priority_two, *standard_route_2, 0], 0.0]
        delivery_route_3 = [[0, *priority_three, *standard_route_3, 0], 0.0]
        delivery_routes = [delivery_route_1, delivery_route_2, delivery_route_3]

        # iterate through delivery routes and calculate distances
        for i in range(3):
            for j in range(len(delivery_routes[i][0]) - 1):
                delivery_routes[i][1] += DISTANCES[delivery_routes[i][0][j], delivery_routes[i][0][j + 1]]

            if delivery_routes[i][1] < final_route[i][1] or final_route[i][1] == 0.0:
                final_route[i] = delivery_routes[i]
                final_packages[i] = package_list[i]

        # clear package lists
        package_list = [[], [], []]

    # assign package delivery times
    truck1.route = final_route[0][0]
    truck1.total_distance = final_route[0][1]
    truck1.load(final_packages[0])

    truck2.route = final_route[1][0]
    truck2.total_distance = final_route[1][1]
    truck2.load(final_packages[1])

    truck3.route = final_route[2][0]
    truck3.total_distance = final_route[2][1]
    truck3.load(final_packages[2])


# not needed?
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
    intro()  # Display intro message
    initialize()  # Initialize data structures
    run_simulation()  # Run simulation
    user_interface()  # User Input Loop
    exit()  # Graceful exit


if __name__ == '__main__':
    main()
