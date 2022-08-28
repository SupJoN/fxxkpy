# coding:utf-8
# 完整的字典
class FullDict():
    __slots__: tuple = ("__default", "__clear", "__fdict", "__index", "__KeyIterator")

    def __init__(self, *args: any, **kwargs) -> None:
        class FullDictKeyIterator(object):
            __slots__: tuple = ("index", "current")

            def __init__(self, index: list) -> None:
                self.index: list = index
                self.current: int = 0

            def __next__(self) -> any:
                if self.current < len(self.index):
                    item = self.index[self.current]
                    self.current += 1
                    return item
                else:
                    raise StopIteration

            def __iter__(self) -> "FullDict.__KeyIterator":
                return self

        from collections import defaultdict

        class FDict(defaultdict):
            def __init__(self, default: any) -> None:
                if default != None:
                    super().__init__(default)
                else:
                    super().__init__()

        class Default(object):
            value: any = None

            @staticmethod
            def Value() -> any:
                return Default.value

        if len(args) == 1:
            Default.value: any = args[0]
            self.__default: any = args[0]
        elif len(args) > 1:
            Default.value: any = args
            self.__default: any = args
        else:
            self.__default: any = None
        try:
            if kwargs["clear"] == True:
                self.__clear: bool = True
            else:
                self.__clear: bool = False
        except:
            self.__clear: bool = False
        self.__fdict: FDict = FDict(Default.Value)
        self.__index: list = []
        self.__KeyIterator = FullDictKeyIterator

    @property
    def default(self) -> any:
        return self.__default

    @property
    def fdict(self) -> any:
        return self.__fdict

    def clear(self) -> None:
        if self.__clear:
            self.__fdict.clear()
            self.__index: list = []
        else:
            raise AttributeError("'FullDict' object has no attribute 'clear'")

    def __len__(self) -> int:
        return len(self.__index)

    def __contains__(self, item: any) -> bool:
        for i in self.__index:
            if i == item:
                return True
        return False

    def __getitem__(self, key: any) -> any:
        return self.__fdict.__getitem__(key)

    def __setitem__(self, key: any, value: any) -> None:
        if self.__index.count(key) == 0:
            self.__index.append(key)
        self.__fdict.__setitem__(key, value)

    def __delitem__(self, key: any) -> None:
        if self.__index.count(key) != 0:
            self.__index.remove(key)
        self.__fdict.__delitem__(key)

    def __bool__(self) -> bool:
        return bool(self.__index)

    def __eq__(self, other: any) -> bool:
        if type(other) != type(self):
            return False
        else:
            return other.fdict == self.fdict

    def __ne__(self, other: any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> "FullDict.__KeyIterator":
        return self.__KeyIterator(self.__index)

    def __repr__(self) -> str:
        return f"FullDict({self.__default}{self.__fdict.__repr__()[79:len(self.__fdict.__repr__())]}"

    def __str__(self) -> str:
        return self.__repr__()
