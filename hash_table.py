class HashTableWithChaining:
    def __init__(self, size, capacity=10):
        self.size = size
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key):
        return int(key) % len(self.table)

    def insert(self, key, value):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        # Check if key already exists in the bucket
        # If key exists, update the value
        # If key does not exist, add it to the bucket
        for item in bucket_list:
            if item[0] == key:
                item[1] = value
                self.size += 1
                return
        bucket_list.append([key, value])

    # Search for an item in the table
    # O(n) time complexity
    def search(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        for item in bucket_list:
            if item[0] == key:
                return item[1]
        return None

    def delete(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)
            self.size -= 1

    def inspect(self):
        packages = []
        # iterate through each bucket in the table and print the key-value pairs
        for bucket in self.table:
            for key, value in bucket:
                packages.append(value)
        for package in packages:
            print(package)

    def __str__(self):
        return str(self.table)

    # Make the hash table iterable
    def __iter__(self):
        for bucket in self.table:
            for item in bucket:
                yield item

