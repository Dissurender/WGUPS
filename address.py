class Address:
    def __init__(self, ID, name, street):
        self.ID = ID
        self.name = name
        self.street = street
        self.city = None
        self.state = None
        self.zip = None

    def __str__(self):
        if self.city is not None:
            return f'{self.ID} {self.name}: {self.street} {self.city}, {self.state} {self.zip}'
        else:
            return f'{self.ID} {self.name}: {self.street}'
