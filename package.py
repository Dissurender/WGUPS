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
        self.leave_time = None  # added when truck leaves hub
        self.delivery_time = None  # added when route is calculated

    def __str__(self) -> str:
        string_builder = ""

        string_builder += 'Package ID: ' + str(self.ID) + '\n'
        string_builder += 'Weight: ' + str(self.weight) + ' lbs\n'
        string_builder += 'Deadline: ' + str(self.handle_deadline()) + '\n'
        string_builder += 'Delivery status: ' + str(self.get_status_at_time(datetime.datetime.now())) + '\n'
        string_builder += f'\n== Address for Package {self.ID} ==\n' + self.get_address() + '\n'

        return string_builder

    def get_address(self) -> str:
        return self.address.__str__()

    def handle_deadline(self):
        if self.deadline > datetime.timedelta(hours=10, minutes=30):
            return 'EOD'
        else:
            return self.deadline

    def get_status_at_time(self, time):
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

        if self.leave_time is None:
            return Status.AT_HUB
        elif time < self.leave_time:
            return Status.AT_HUB
        elif time < self.delivery_time:
            return Status.OUT_FOR_DELIVERY
        elif time >= self.delivery_time:
            return Status.DELIVERED
