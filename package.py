import datetime

from address import Address
from status import Status


class Package:
    def __init__(self, ID, weight, note, is_priority=False) -> None:
        self.ID = ID
        self.deadline: int or str = None
        self.weight = weight
        self.note = note
        self.is_priority = is_priority

        self.address: Address or None = None
        self.leave_time = None
        self.delivery_time = None

    def __str__(self) -> str:
        string_builder = ""

        string_builder += 'Package ID: ' + str(self.ID) + '\n'
        string_builder += 'Weight: ' + str(self.weight) + ' lbs\n'
        string_builder += 'Deadline: ' + str(self.deadline) + '\n'
        string_builder += 'Status: ' + str(self.get_status_at_time(datetime.datetime.now())) + '\n\n'
        string_builder += 'Address: ' + self.get_address() + '\n'

        return string_builder

    def get_address(self) -> str:
        return self.address.__str__()

    def get_status_at_time(self, time):
        if self.leave_time is None:
            return Status.AT_HUB
        elif time < self.leave_time:
            return Status.AT_HUB
        elif time < self.delivery_time:
            return Status.OUT_FOR_DELIVERY
        elif time >= self.delivery_time:
            return Status.DELIVERED

        if self.ID == 9:
            delay_time = datetime.datetime(hour=10, minute=20)
            if time < delay_time:
                return Status.AT_HUB
            elif delay_time < time < self.delivery_time:
                self.address.street = '410 S State St'
                self.address.city = 'Salt Lake City'
                self.address.state = 'UT'
                self.address.zip = '84111'
                return Status.OUT_FOR_DELIVERY
            elif time >= self.delivery_time:
                return Status.DELIVERED
