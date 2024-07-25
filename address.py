class Address:
    def __init__(self, ID, name, street):
        self.ID = int(ID)
        self.name = name
        self.street = street
        self.city = None
        self.state = None
        self.zip = None

    def __str__(self):
        string_builder = ""

        string_builder += 'Address ID: ' + str(self.ID) + '\n'
        string_builder += 'Name: ' + str(self.name) + '\n'
        string_builder += 'Street: ' + str(self.street) + '\n'
        if self.city is not None:
            string_builder += 'City: ' + str(self.city) + '\n'
            string_builder += 'State: ' + str(self.state) + '\n'
            string_builder += 'Zip: ' + str(self.zip) + '\n'

        return string_builder
