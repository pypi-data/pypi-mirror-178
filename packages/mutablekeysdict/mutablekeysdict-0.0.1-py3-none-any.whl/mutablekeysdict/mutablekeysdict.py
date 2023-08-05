from typing import Any, Dict, ItemsView, Iterator, KeysView, Mapping, Optional, ValuesView

class I:
    def __init__(self):
        self.i = 0

    def __next__(self):
        i = self.i
        self.i += 1
        return i
    
    def __iter__(self):
        return self


class MutableKeysDict(Dict):
    def __init__(self, data: Optional[Mapping] = None) -> None:
        self.i = I()
        self._keys = {} # {current value: i}
        if data is not None:
            self._keys = {key: i for i, key in zip(self.i, data.keys())}
            self.data: dict = {self._keys[key]: value for key, value in data.items()}
        else:
            self.data = {}

    def need_keys_reset(self) -> bool:
        for key in self.keys():
            try:
                self._keys[key]
            except KeyError:
                return True
        return False
    
    def reset_keys(self) -> None:
        if self.need_keys_reset():
            self._keys = {key: i for i, key in zip(self.i, self.keys())}
            self.data: dict = {self._keys[key]: value for key, value in zip(self._keys, self.values())}

    def replace_key(self, old_key, new_key) -> None:
        value = self[old_key]
        self[new_key] = value
        del self[old_key]
    
    def __dict__(self) -> dict:
        return {keys: value for keys, value in zip(self._keys.keys(), self.data)}

    def __repr__(self) -> str:
        self.reset_keys()
        return f'MutableKeysDict({dict(self)})'

    def __getitem__(self, key) -> Any:
        self.reset_keys()
        return self.data[self._keys[key]]
    
    def __setitem__(self, key, value) -> None:
        self.reset_keys()
        if key not in self.keys():
            self._keys[next(self.i)] = key
        self.data[self._keys[key]] = value

    def __delitem__(self, key) -> None:
        self.reset_keys()
        del self.data[self._keys[key]]
        del self._keys[key]
    
    def __iter__(self) -> Iterator:
        return iter(self.keys())
    
    def __len__(self) -> int:
        return len(self.keys())
    
    def __contains__(self, value: Any) -> bool:
        return value in self.keys()
    
    def __eq__(self, other) -> bool:
        return dict(self) == other
    
    def __ne__(self, other) -> bool:
        return dict(self) != other
    
    def keys(self) -> KeysView:
        return self._keys.keys()
    
    def items(self) -> ItemsView:
        return dict(self).items()
    
    def values(self) -> ValuesView:
        return self.data.values()
    
    def get(self, key, default=None) -> Any:
        self.reset_keys()
        if default is None:
            return self.data.get(self._keys[key])
        else:
            return self.data.get(self._keys[key], default)
        
    def pop(self, key) -> Any:
        self.reset_keys()
        value = self.data.pop(self._keys[key])
        del self._keys[key]
        return value
        
    def popitem(self, key) -> tuple:
        self.reset_keys()
        item = self.popitem(key)
        del self._keys[key]
        return item
    
    def clear(self) -> None:
        self._keys.clear()
        self.data.clear()

    def update(self, other) -> None:
        self.data.update(other)

    def setdefault(self, key, default) -> Any:
        self.reset_keys()
        return self.data.setdefault(self._keys[key], default)