import datetime
from typing import List

from package import Package


# Truck.packages -> list of (package, distance_to_next_address)


class Truck:
    def __init__(self, ID) -> None:
        self.ID = ID  # Truck ID
        self.packages: List[Package, float] = []
        self.leave_time = None
        self.total_distance = 0.0
        self.driver = None

    def __str__(self) -> str:
        return f'Truck ID: {self.ID}'

    def load(self, package_list) -> None:
        self.packages = package_list

    # Iterate through packages and deliver them (remove from list)
    def deliver_packages(self):
        while len(self.packages) > 0:
            package, distance = self.packages.pop(0)
            self.total_distance += distance
            # Calculate time to deliver package in minutes
            delivery_time = datetime.timedelta(hours=distance / 18)
            package.delivery_time = self.leave_time + delivery_time
