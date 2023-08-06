from collections import namedtuple, MutableMapping
from collections.abc import KeysView, ValuesView, ItemsView

class MostRecentDict(MutableMapping):

    __slots__ = ('_size', '_next', '_items', '_keys')

    item_tpl = namedtuple('item', ('key', 'value'))

    def __init__(self, size):
        if not isinstance(size, int):
            raise TypeError("Expected an integer for \"size\"")
        # Structures to store the data
        self._items, self._keys = [None]*size, {}
        # Store the counter / size
        self._size, self._next = size, 0

    ### Additional Functionality

    # GET NEXT ITEM / VALUE / KEY
    def get_next_key(self):
        return self._items[self._next].key
    def get_next_value(self):
        return self._items[self._next].value
    def get_next(self):
        return self._items[self._next]

    # TO DICT
    def to_dict(self):
        dct = {item.key:item.value for item in self._items[self._next:]}
        dct.update({item.key:item.value for item in self._items[:self._next]})
        return dct

    ### TRADITIONAL NON-REQUIRED FUNCTIONALITY
    def __str__(self):
        return 'MRD('+','.join((f'{k}:{i}' for k,i in self.to_dict().items()))+')'
    def __repr__(self):
        return self.__str__()

    ### BASE FUNCTIONALITY
    def __setitem__(self, key, item):
        if key in self._keys:
            # Get the item in the current slot
            swap_key, swap_item = self._items[self._next]
            # Get the old index
            swap_index = self._keys[key]
            # Save in the old slot
            self._items[swap_index] = self._items[self._next]
            # Save new key pointer
            self._keys[key] = swap_index
        # Place the new item
        self._items[self._next] = self.item_tpl(key, item)
        self._keys[key] = self._next
        # Get the next item we will be removing
        self._next = (self._next + 1) % self._size


    def __getitem__(self, key):
        # Raise the key error if it is not there
        if key not in self._keys:
            raise KeyError(f"Missing key \"{key}\"")
        # Extract the item
        item = self._items.__getitem__(self._keys[key]).value
        # Set the item, it will update its place
        self.__setitem__(key, item)
        # Return the item
        return item

    def __delitem__(self, key):
        # Raise the key error if it is not there
        if key in self._keys:
            raise KeyError(f"Missing key \"{key}\"")
        # Set the index to None
        self._items[self._keys.__getitem__(key)] = None
        # Delete the key pointing to the index
        self._keys.__delitem__(key)

    def __iter__(self):
        for key, item in self._items[self._next:]:
            yield key
        for key, item in self._items[:self._next]:
            yield key

    def __len__(self):
        return len(self._keys)
