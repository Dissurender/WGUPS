import datetime

from status import Status


class Package:
    def __init__(self, ID, deadline, weight, note, is_priority=False) -> None:
        self.ID = ID
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.is_priority = is_priority

        self.address = None
        self.leave_time = None
        self.delivery_time = None

    def __str__(self) -> str:
        return f"Package {self.ID}"

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
            if time < datetime.datetime("10:20"):
                return Status.DELAYED
            elif time < self.delivery_time:
                return Status.OUT_FOR_DELIVERY
            elif time >= self.delivery_time:
                return Status.DELIVERED
