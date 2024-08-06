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
    if len(time[1]) > 2 and time[1].split(' ')[1] == 'PM':
        hour += 12
    return datetime.timedelta(hours=hour, minutes=minute)


print('Loading addresses...')
with open('csv/addresses.csv', 'r') as address_file:
    address_data = csv.reader(address_file)
    address_data = list(address_data)

# Create a list of Address objects
for address in address_data:
    addr = Address(int(address[0]), address[1], address[2])
    ADDRESSES.insert(addr.ID, addr)

print('Loading packages...')
with open('csv/packages.csv', 'r') as package_file:
    package_data = csv.reader(package_file)
    package_data = list(package_data)

for package in package_data:
    # 1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21,
    parcel = Package(int(package[0]), package[6], package[7])

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
        if distance_data[i][j]:
            DISTANCES[i, j] = float(distance_data[i][j])
        else:
            DISTANCES[i, j] = 0.0


def get_address_by_street(address_list, street: str) -> Address or None:
    for addr in address_list:
        if addr.street == street:
            return addr
    return None


def get_packages_by_address(package_list, address: int) -> list:
    packages = []
    for package in package_list:
        if package.address.ID == address:
            packages.append(package)
    return packages


def get_distance(i: int, j: int) -> float:
    if i == j:  # same address, no distance
        return 0.0
    if i > j:  # swap i and j to properly call the distance from the dictionary if i is greater than j
        return DISTANCES[j, i]
    return DISTANCES[i, j]


def truck_assigner(package) -> int | None:
    id: int = int(package.ID)

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

    return None


# def route_formatter(package):


#
# Greedy algorithms/optimization
#

# Nearest neighbor algorithm
# O(N^2) time complexity
# Consume a list of packages and return a route of addresses
def nearest_neighbor(start, packages_list):
    packages = packages_list.copy()
    route = [start]
    current = start
    while len(packages) > 0:
        nearest = None
        for package in packages:
            if nearest is None:
                nearest = package
            if get_distance(current, package.address.ID) < get_distance(current, nearest.address.ID):
                nearest = package
        route.append(nearest.address.ID)
        current = nearest.address.ID
        packages.remove(nearest)
    return route


# distribute packages to trucks
def sort_packages(packages, trucks):
    standard_packages = []
    for package in packages:
        if package.is_priority:
            choice = truck_assigner(package)
            if choice is None:
                choice = random.randint(1, 2)
            if choice == 1:
                trucks[0].priority_packages.append(package)
            else:
                trucks[1].priority_packages.append(package)
        else:
            choice = truck_assigner(package)
            if choice is None:
                standard_packages.append(package)  # add to standard packages list
            else:
                match choice:
                    case 1:
                        trucks[0].packages.append(package)
                    case 2:
                        trucks[1].packages.append(package)
                    case 3:
                        trucks[2].packages.append(package)
    # fill trucks with standard packages
    for package in standard_packages:
        if trucks[0].package_count() < 14:
            trucks[0].packages.append(package)
        elif trucks[1].package_count() < 14:
            trucks[1].packages.append(package)
        else:
            trucks[2].packages.append(package)


# deliver packages
# O(N^2) time complexity
# TODO: refactor to work
def deliver_packages(truck):
    current = truck.route[0]
    total_distance = 0.0
    for i in range(1, len(truck.route)):
        next_local = truck.route[i]
        print(f'Truck {truck.ID} traveling from {current} to {next_local}')
        distance = get_distance(current, next_local)
        total_distance = total_distance + distance
        print(f'Total distance: {total_distance}')
        curr_packages = get_packages_by_address(truck.packages, next_local)
        for package in curr_packages:
            print(f'Delivering package {package.ID} to {package.address.street}')
            # convert distance to time in minutes and add to leave time
            delivery_time = truck.leave_time + datetime.timedelta(minutes=total_distance / 18 * 60)
            print(f'Time {delivery_time}')
            package.delivery_time  = delivery_time
            # print(f'Package {package.ID} delivered at {package.delivery_time}')
        truck.packages = [package for package in truck.packages if package not in curr_packages]
        current = next_local
    truck.total_distance = total_distance


#
# Main control flow
#


# Helper function to print out truck packages and routes for debugging
def print_out_packages(trucks):
    print()
    # print truck packages
    for truck in trucks:
        pri = []
        std = []
        for package in truck.packages:
            std.append(package.ID)
        for package in truck.priority_packages:
            pri.append(package.ID)
        print(f'Truck {truck.ID} packages: {std}')
        print(f'Truck {truck.ID} Route: {truck.route}')
        print()
        pri.clear()
        std.clear()


def run_simulation():
    print('Running simulation...')
    # create trucks
    truck1 = Truck(1, ADDRESSES[0])
    truck2 = Truck(2, ADDRESSES[0])
    truck3 = Truck(3, ADDRESSES[0])

    trucks = [truck1, truck2, truck3]

    # load priority packages
    packages = [PACKAGES.search(i) for i in range(1, 41)]

    # sort packages to priority and standard lists
    sort_packages(packages, trucks)

    # print truck packages
    # print_out_packages(trucks)

    print('Optimizing routes...')
    # Nearest neighbor optimization
    for truck in trucks:
        # starting at hub, find nearest neighbor path for priority packages
        temp_list = nearest_neighbor(0, truck.priority_packages)

        # add the optimized route to the truck's route
        truck.route.extend(temp_list)

        # remove all but the last element
        temp_list = temp_list[-1:]

        # starting at last element of temp list, find nearest neighbor path for standard packages
        temp_list = nearest_neighbor(temp_list[0], truck.packages)

        truck.route.extend(temp_list[1:])
        truck.route.append(0)

        truck.packages.extend(truck.priority_packages)
        truck.priority_packages.clear()

        print(f'Truck {truck.ID} route created: {truck.route}')

    # iterate through the route and calculate the total distance
    trucks[0].leave_time = datetime.timedelta(hours=8, minutes=0)
    deliver_packages(trucks[0])

    trucks[1].leave_time = datetime.timedelta(hours=9, minutes=5)
    deliver_packages(trucks[1])

    truck3_leave_time = max(
        datetime.timedelta(hours=10, minutes=20),
        truck1.leave_time + datetime.timedelta(minutes=truck1.total_distance / 18))
    print(f'Truck 3 leave time: {truck3_leave_time}')
    trucks[2].leave_time = truck3_leave_time
    deliver_packages(trucks[2])

    print_out_packages(trucks)
    print('Simulation complete.')
    print(f'Total distance traveled: {truck1.total_distance + truck2.total_distance + truck3.total_distance} miles')


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
            Welcome to the WGUPS package tracking system!
            """)
    print('Starting Service...')


def user_interface():
    print('User interface...')
    menu = """
            Please select an option:
            1. Lookup package at time
            2. Lookup address
            3. Print all packages
            4. Print all addresses
            5. Exit
            
            """

    while True:
        user_input = input(menu + '\nEnter choice: ')

        match user_input:
            case '1':
                print('Lookup package at time')
                package_id = input('Enter package ID: ')
                package = PACKAGES.search(int(package_id))
                search_time = input('Enter time to search for package: ')
                search_time = convert_time(search_time)
                package.get_status_at_time(search_time)
                print(f'Package {package_id} status at {search_time}: {package.get_status_at_time(search_time)}')
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


# Test code
# print('Testing...')
def test_truck_assigner():
    assert truck_assigner(PACKAGES.search(3)) == 2
    assert truck_assigner(PACKAGES.search(18)) == 2


if __name__ == '__main__':
    main()
