class HashTableWithChaining:
    def __init__(self, size, capacity=10):
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key):
        return int(key) % len(self.table)

    # Part A: insert data
    def insert(self, key, value):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        # Check if key already exists in the bucket
        # If key exists, update the value
        # If key does not exist, add it to the bucket
        for item in bucket_list:
            if int(item[0]) == key:
                item[1] = value
                return
        bucket_list.append([int(key), value])

    # Search for an item in the table
    # O(n) time complexity
    # Part B: search
    def search(self, key):
        bucket = self._hash(key)
        bucket_row = self.table[bucket]

        # iterate the data in the bucket, return wanted data item
        # checks in O(N) where N is bucket_row length
        for data in bucket_row:
            if data[0] == key:
                return data[1]

        # if key not in table return nothing
        print('Key not found')
        return None

    def delete(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)

    def inspect(self):
        packages = [-1] * 40
        # iterate through each bucket in the table and place the package in the correct index for printing
        # O(N) where N is a known constant 40
        for bucket in self.table:
            for item in bucket:
                packages[int(item[0]) - 1] = item[1]
        for package in packages:
            print(package.__str__())

    def __str__(self):
        return str(self.table)

    # Make the hash table iterable
    def __iter__(self):
        for bucket in self.table:
            for item in bucket:
                yield item
