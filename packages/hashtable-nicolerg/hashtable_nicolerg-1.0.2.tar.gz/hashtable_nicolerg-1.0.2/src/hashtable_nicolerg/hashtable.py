"""Implement a custom hash table"""

from typing import NamedTuple, Any
from collections import deque

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:

    def __init__(self, capacity: int, load_factor_threshold=0.6):
        if not isinstance(capacity, int):
            raise TypeError("Size must be an integer")
        if capacity < 1:
            raise ValueError("Size must be a positive number")
        self._buckets = [deque() for _ in range(capacity)]
        self._load_factor_threshold = load_factor_threshold

    @classmethod
    def from_dict(cls, dictionary, capacity=None):
        hash_table = cls(capacity or len(dictionary) * 100)
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    def __len__(self):
        return len(self.pairs)

    def __setitem__(self, key, value):
        bucket = self._get_bucket(key)
        for index, pair in enumerate(bucket):
            if pair.key == key:
                bucket[index] = Pair(key, value)
                break
        else:
            bucket.append(Pair(key, value))

        if self.load_factor >= self.load_factor_threshold:
            self._resize_and_rehash()

    def __getitem__(self, key):
        bucket = self._get_bucket(key)
        for pair in bucket:
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def __delitem__(self, key):
        bucket = self._get_bucket(key)
        for index, pair in enumerate(bucket):
            if pair.key == key:
                del bucket[index]
                break
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self):
        yield from self.keys

    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return set(self.pairs) == set(other.pairs)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), capacity=self.capacity)

    def clear(self):
        self._buckets = [deque() for _ in range(self.capacity)]

    def update(self, other):
        if isinstance(other, dict):
            other = HashTable.from_dict(other)
        for key, value in other.pairs:
            self[key] = value

    @property
    def pairs(self):
        return [pair for bucket in self._buckets for pair in bucket]

    @property
    def values(self):
        return [pair.value for pair in self.pairs]

    @property
    def keys(self):
        return {pair.key for pair in self.pairs}
    
    @property
    def capacity(self):
        return len(self._buckets)

    @property
    def load_factor(self):
        return len(self)/self.capacity

    @property
    def load_factor_threshold(self):
        return self._load_factor_threshold

    def _index(self, key):
        return hash(key) % self.capacity

    def _get_bucket(self, key):
        return self._buckets[self._index(key)]

    def _resize_and_rehash(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
        self._buckets = copy._buckets
