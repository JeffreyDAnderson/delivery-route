# TIME COMPLEXITY: O(N)     --worst run time of a function is O(N)--
class HashTable:
    def __init__(self, length=50):
        self.array = [None] * length

    # hash function to transform a key into a relatively unique
    # index in the table's array. With the given data set of
    # 40 packages and the default size of the array of 50 this
    # hash will uniquely place all packages without collisions

    # TIME COMPLEXITY: O(1)
    # SPACE COMPLEXITY:
    def hashKey(self, key):
        length = len(self.array)
        return int((int(key) ^ 13) % length)

    # Insertion into the table array will check a few things before
    # storing the given (key, value). The hashed key will provide the
    # index to the array. If the index is not empty then each element
    # stored in that index will be checked for a match. If there is a
    # match then that key will be updated with the given value.
    # If the index is empty then a new list will be created in that spot
    # and the given (key, value) will be appended to the inner list.

    # TIME COMPLEXITY: O(N)     --worst case the given object is stored in the same location every time--
    # SPACE COMPLEXITY:
    def insert(self, key, val):
        index = self.hashKey(key)
        if self.array[index] is not None:
            for i in self.array[index]:
                if i[0] == key:
                    i[1] == val
                    break
                else:
                    self.array[index].append([key, val])
        else:
            self.array[index] = []
            self.array[index].append([key, val])

    # Given a key this function hashes that value to get an index
    # for the matching value. If the given key is not in the array
    # then a KeyError is thrown. If the index is not empty then all
    # elements of the inner list will be checked for the matching key

    # TIME COMPLEXITY: O(N)     --worst case has to check all items in one location-- (should not ever happen)
    # SPACE COMPLEXITY:
    def retrieve(self, key):
        index = self.hashKey(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            for i in self.array[index]:
                if i[0] == key:
                    return i[1]
            raise KeyError()
