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
        for k, v in bucket_list:
            # If key exists, update the value
            if k == key:
                v = value
                return
        # If key does not exist, add it to the bucket
        bucket_list.append([key, value])

    # Search for an item in the table
    def search(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        for k, v in bucket_list:
            if k == key:
                return v
        return None

    def delete(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)
            self.size -= 1

    def __str__(self):
        return str(self.table)
