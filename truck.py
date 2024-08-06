from typing import List

from package import Package


class Truck:
    def __init__(self, ID, address) -> None:
        self.ID = ID  # Truck ID
        self.packages: List[Package] = []
        self.priority_packages: List[Package] = []
        self.route = []
        self.location = address
        self.leave_time = None
        self.total_distance = 0.0

    def __str__(self) -> str:
        string_builder = ""

        string_builder += 'Truck: ' + str(self.ID) + '\n'
        string_builder += 'Current Location: ' + str(self.location.name) + '\n'
        string_builder += 'Time Departed: ' + str(self.leave_time) + '\n'
        string_builder += 'Total Distance: ' + str(self.total_distance) + '\n'
        string_builder += 'Packages: \n'
        string_builder += 'Priority Packages: ' + str(len(self.priority_packages)) + '\n'
        string_builder += 'Non-Priority Packages: ' + str(len(self.packages)) + '\n'

        return string_builder
