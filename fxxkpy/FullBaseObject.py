# coding:utf-8
import threading as __threading


# 完整的字典
class FullDict(object):
    """
    FullDict
    ========

    可以遍历的默认字典

    使用 self.__index 保存列表的所有已知 (经过赋值的) 键

    属性:
        `__default`: 默认值
        `__clear`: 是否启用 ```clear``` 方法, 默认为 ```False```
        `__fdict`: 存放 ```defaultdict``` 的属性
        `__index`: 保存列表的所有已知(经过赋值的)键
        `__KeyIterator`: FullDict 的迭代器
    """

    import typing as __typing
    from typing import overload as __overload

    __slots__: tuple[str, ...] = ("__default", "__clear", "__fdict", "__index")

    class KeyIterator(object):
        import typing as __typing

        __slots__: tuple[str, ...] = ("index", "current")

        def __init__(self, index: list) -> None:
            self.index: list = index
            self.current: int = 0

        def __next__(self) -> __typing.Any:
            import typing as __typing

            if self.current < len(self.index):
                item: __typing.Any = self.index[self.current]
                self.current += 1
                return item
            else:
                raise StopIteration

        def __iter__(self) -> "FullDict.__KeyIterator":
            return self

    def __init__(self, *args: __typing.Any, **kwargs: __typing.Any) -> None:
        from collections import defaultdict

        length: int = len(args)
        if length:
            if length - 1:
                self.__default: tuple = args
            else:
                import typing as __typing
                self.__default: __typing.Any = args[0]
        else:
            self.__default: None = None
        self.__fdict: defaultdict = defaultdict(lambda: self.__default)

        try:
            if kwargs["clear"] == True:
                self.__clear: bool = True
            else:
                self.__clear: bool = False
        except:
            self.__clear: bool = False

        self.__index: list = []

    @property
    def default(self) -> __typing.Any:
        return self.__default

    @default.setter
    def default(self, value: __typing.Any) -> None:
        import typing
        self.__default: typing.Any = value

    @property
    def fdict(self) -> __typing.Any:
        return self.__fdict

    def clear(self) -> None:
        if self.__clear:
            self.__fdict.clear()
            self.__index.clear()
        else:
            raise AttributeError("This 'FullDict' can not clear")

    def copy(self) -> "FullDict":
        from collections import defaultdict
        result = FullDict(self.__default)
        result._FullDict__fdict: defaultdict = self.__fdict.copy()
        result._FullDict__index: list = self.__index.copy()
        return result

    @staticmethod
    def fromkeys(seq: __typing.Iterable, default: __typing.Any) -> "FullDict":
        result: FullDict = FullDict(default)
        for i in seq:
            result[i] = default
        return result

    def get(self, key: __typing.Any, default: __typing.Any = None) -> __typing.Any:
        return self[key] if key in self.__index else default

    def setdefault(self, key, default: __typing.Any = None) -> __typing.Any:
        import typing
        self[key]: typing.Any = self[key] if key in self.__index else default
        return self[key]

    @__overload
    def pop(self, key: __typing.Any) -> __typing.Any:
        ...

    @__overload
    def pop(self, key: __typing.Any, default: __typing.Any) -> __typing.Any:
        ...

    def pop(self, *args: __typing.Any, **kwargs: __typing) -> __typing.Any:
        import typing as __typing

        def key_pop(key: __typing.Any) -> __typing.Any:
            if args[0] not in self.__index:
                raise KeyError(repr(key))
            else:
                import typing
                result: typing.Any = self[key]
                del self[key]
                return result

        def default_pop(key: __typing.Any, default: __typing.Any) -> __typing.Any:
            if key in self.__index:
                import typing
                result: typing.Any = self[key]
                del self[key]
                return result
            else:
                return default

        length = len(args) + len(kwargs)
        if length == 1:
            return key_pop(*args, **kwargs)
        elif length == 2:
            return default_pop(*args, **kwargs)
        else:
            raise TypeError(f"pop() takes from 1 to 2 positional arguments but {len(args)} were given")

    def popitem(self) -> tuple[__typing.Any, __typing.Any]:
        if len(self.__index) != 0:
            result = self.__index[-1], self[self.__index[-1]]
            del self[self.__index[-1]]
            return result
        else:
            raise KeyError("popitem(): dictionary is empty")

    def items(self) -> list[tuple[__typing.Any, __typing.Any]]:
        import typing
        result: list[tuple[typing.Any, typing.Any]] = []
        for i in self.__index:
            result.append((i, self.__fdict[i]))
        return result

    def keys(self) -> list[__typing.Any]:
        return self.__index

    def values(self) -> list[__typing.Any]:
        import typing
        result: list[typing.Any] = []
        for i in self.__index:
            result.append(self.__fdict[i])
        return result

    def __len__(self) -> int:
        return len(self.__index)

    def __contains__(self, item: __typing.Any) -> bool:
        return item in self.__index

    def __getitem__(self, key: __typing.Any) -> __typing.Any:
        return self.__fdict.__getitem__(key)

    def __setitem__(self, key: __typing.Any, value: __typing.Any) -> None:
        if key not in self.__index:
            self.__index.append(key)
        self.__fdict.__setitem__(key, value)

    def __delitem__(self, key: __typing.Any) -> None:
        if key in self.__index:
            self.__index.remove(key)
            self.__fdict.__delitem__(key)
        else:
            raise KeyError(repr(key))

    def __bool__(self) -> bool:
        return not not self.__index

    def __eq__(self, other: __typing.Any) -> bool:
        if isinstance(other, FullDict):
            return other._FullDict__fdict == self.__fdict
        else:
            return False

    def __ne__(self, other: __typing.Any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> "FullDict.KeyIterator":
        return self.KeyIterator(self.__index)

    def __repr__(self) -> str:
        fdict_str: str = self.__fdict.__repr__()
        return f"FullDict({self.__default}{fdict_str[fdict_str.index('>, ')+1::]})"

    def __str__(self) -> str:
        return self.__repr__()

    del __typing
    del __overload


# 完整的数字
class FullRationalNumber(object):
    """
    FullRationalNumber
    ==================

    初始化时若不传参, 值为 0 ; 若传一个参数, 则其为数值; 若传两个参数, 则默认第一个值为分子, 第二个值为分母

    初始化只支持 ```int```, ```float```, ```FullRationalNumber```, ```decimal.Decimal```, ```fraction.Fraction```, ```fractions.Fraction```, ```sympy.core.numbers.Zero```, ```sympy.core.numbers.One```, ```sympy.core.numbers.Integer```, ```sympy.core.numbers.Float``` 或 可以转成 ```float```, ```int``` 及其 类分数形式 的 ```str```, 返回值是 ```FullRationalNumber```

    类分数形式 是: ```f"{numerator: int | float}/{denominator: int | float}"```

    幂运算只支持 可转成 ```FullRationalNumber``` 且 转换后分母为 1 的数据

    算术运算先会将数据转为 ```FullRationalNumber``` 后再计算

    比较运算 (```==``` 与 ```!=``` 除外) 会先尝试把数据转为 ```FullRationalNumber``` 在比较, 若无法转换, 则将 ```self``` 转为 ```float``` 后再尝试比较, 若还无法比较, 则引发 ```TypeError``` 报错
    """

    import typing as __typing
    from decimal import Decimal as __Decimal
    from typing import overload as __overload

    @__overload
    def __init__(self) -> None:
        ...

    @__overload
    def __init__(self, numerator: __typing.Any, denominator: __typing.Any) -> None:
        ...

    @__overload
    def __init__(self, value: __typing.Any) -> None:
        ...

    def __init__(self, *args: __typing.Any) -> None:
        import decimal

        from ._evaluate import evaluate

        if len(args) == 0:
            self.__numerator: decimal.Decimal = decimal.Decimal("0")
            self.__denominator: decimal.Decimal = decimal.Decimal("1")
            return
        elif len(args) == 1:
            self.__numerator, self.__denominator = evaluate(args[0], "FullRationalNumber")
        elif len(args) == 2:
            self.__numerator, self.__denominator = evaluate(args[0], "FullRationalNumber")
            result = evaluate(args[1], "FullRationalNumber")
            self.__denominator *= result[0]
            self.__numerator *= result[1]
            if self.__denominator == 0:
                raise ZeroDivisionError("division by zero")
            del result
        else:
            raise TypeError(f"FullRationalNumber.__init__() takes from 0 to 2 positional arguments but {len(args)} were given")

        while self.__numerator % 1 != 0 or self.__denominator % 1 != 0:
            self.__numerator *= 10
            self.__denominator *= 10

        try:
            self.__numerator: decimal.Decimal = decimal.Decimal(str(self.__numerator)[:str(self.__numerator).index("."):])
        except:
            pass

        try:
            self.__denominator: decimal.Decimal = decimal.Decimal(str(self.__denominator)[:str(self.__denominator).index("."):])
        except:
            pass

        if min(abs(self.__numerator), abs(self.__denominator)) >= 2:
            for i in range(2, int(min(abs(self.__numerator), abs(self.__denominator)) + 1)):
                while self.__numerator % i == 0 and self.__denominator % i == 0:
                    self.__numerator //= i
                    self.__denominator //= i

        if self.__denominator < 0:
            self.__numerator: decimal.Decimal = -self.__numerator
            self.__denominator: decimal.Decimal = -self.__denominator

    def simplification(self) -> None:
        import decimal

        if self.__numerator == 0:
            self.__denominator: decimal.Decimal = 1
            return
        else:
            while self.__numerator != int(self.__numerator) or self.__denominator != int(self.__denominator):
                self.__numerator *= 10
                self.__denominator *= 10

            try:
                self.__numerator: decimal.Decimal = decimal.Decimal(str(self.__numerator)[:str(self.__numerator).index("."):])
            except:
                pass

            try:
                self.__denominator: decimal.Decimal = decimal.Decimal(str(self.__denominator)[:str(self.__denominator).index("."):])
            except:
                pass

            if min(abs(self.__numerator), abs(self.__denominator)) >= 2:
                for i in range(2, int(min(abs(self.__numerator), abs(self.__denominator)) + 1)):
                    while self.__numerator % i == 0 and self.__denominator % i == 0:
                        self.__numerator //= i
                        self.__denominator //= i

            if self.__denominator < 0:
                self.__numerator: decimal.Decimal = -self.__numerator
                self.__denominator: decimal.Decimal = -self.__denominator

    def clear(self) -> None:
        import decimal

        self.__numerator: decimal.Decimal = decimal.Decimal("0")
        self.__denominator: decimal.Decimal = decimal.Decimal("1")

    @property
    def numerator(self) -> __Decimal:
        return self.__numerator

    @property
    def denominator(self) -> __Decimal:
        return self.__denominator

    def __add__(self, other: __typing.Any) -> "FullRationalNumber":
        if isinstance(other, FullRationalNumber):
            return FullRationalNumber(self.__numerator * other.denominator + other.numerator * self.__denominator, self.__denominator * other.denominator)
        else:
            return self.__add__(FullRationalNumber(other))

    def __radd__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__add__(FullRationalNumber(other))

    def __iadd__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__add__(FullRationalNumber(other))

    def __sub__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__add__(-FullRationalNumber(other))

    def __rsub__(self, other: __typing.Any) -> "FullRationalNumber":
        return FullRationalNumber(other).__add__(-self)

    def __isub__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__sub__(FullRationalNumber(other))

    def __mul__(self, other: __typing.Any) -> "FullRationalNumber":
        if isinstance(other, FullRationalNumber):
            return FullRationalNumber(self.__numerator * other.numerator, self.__denominator * other.denominator)
        else:
            return self.__mul__(FullRationalNumber(other))

    def __rmul__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__mul__(FullRationalNumber(other))

    def __imul__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__mul__(FullRationalNumber(other))

    def __truediv__(self, other: __typing.Any) -> "FullRationalNumber":
        inverse: FullRationalNumber = FullRationalNumber(other)
        if inverse.numerator != 0:
            return self.__mul__(FullRationalNumber(inverse.denominator, inverse.numerator))
        else:
            raise ZeroDivisionError("division by zero")

    def __rtruediv__(self, other: __typing.Any) -> "FullRationalNumber":
        if self.__numerator != 0:
            return FullRationalNumber(other).__mul__(FullRationalNumber(self.__denominator, self.__numerator))
        else:
            raise ZeroDivisionError("division by zero")

    def __itruediv__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__truediv__(FullRationalNumber(other))

    def __pow__(self, other: __typing.Any) -> "FullRationalNumber":
        FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
        if FullRationalNumber_other.denominator == 1:
            if FullRationalNumber_other.numerator > 0:
                result = FullRationalNumber("1")
                for i in range(int(FullRationalNumber_other.numerator)):
                    result: FullRationalNumber = result.__mul__(self)
                return result
            elif FullRationalNumber_other.numerator == 0:
                if self.__numerator == 0:
                    raise ZeroDivisionError("division by zero")
                else:
                    return FullRationalNumber("1")
            else:
                return FullRationalNumber("1").__truediv__(self.__pow__(-FullRationalNumber_other.numerator))
        else:
            raise TypeError(f"unsupported operand value for \'**\': {repr(self)} and {repr(other)} whose denominator isn't 1")

    def __rpow__(self, other: __typing.Any) -> "FullRationalNumber":
        if self.denominator == 1:
            FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
            if self.numerator > 0:
                result = FullRationalNumber("1")
                for i in range(int(self.numerator)):
                    result: FullRationalNumber = result.__mul__(FullRationalNumber_other)
                return result
            elif self.numerator == 0:
                if self.numerator == 0:
                    raise ZeroDivisionError("division by zero")
                else:
                    return FullRationalNumber("1")
            else:
                return FullRationalNumber("1").__truediv__(FullRationalNumber_other.__pow__(-self.__numerator))
        else:
            raise TypeError(f"unsupported operand value for \'**\': {repr(other)} and {repr(self)} whose denominator isn't 1")

    def __ipow__(self, other: __typing.Any) -> "FullRationalNumber":
        FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
        try:
            return self.__pow__(FullRationalNumber_other)
        except TypeError:
            raise TypeError(f"unsupported operand value for \'**=\': {repr(self)} and {repr(other)} whose denominator isn't 1")

    def __lt__(self, other: __typing.Any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return (self.numerator * FullRationalNumber_other.denominator).__lt__(FullRationalNumber_other.numerator * self.denominator)
        except:
            try:
                return (self.__numerator * other.denominator).__lt__(other.numerator * self.__denominator)
            except:
                from .error import compare_error
                compare_error(self, other, "<")

    def __le__(self, other: __typing.Any) -> bool:
        try:
            return not self.__gt__(other)
        except:
            from .error import compare_error
            compare_error(self, other, "<=")

    def __eq__(self, other: __typing.Any) -> bool:
        try:
            FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
            return (self.__numerator * FullRationalNumber_other.denominator).__eq__(FullRationalNumber_other.numerator * self.__denominator)
        except:
            try:
                return (self.__numerator * other.denominator).__eq__(other.numerator * self.__denominator)
            except:
                return False

    def __ne__(self, other: __typing.Any) -> bool:
        try:
            FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
            return (self.__numerator * FullRationalNumber_other.denominator).__ne__(FullRationalNumber_other.numerator * self.__denominator)
        except:
            return True

    def __gt__(self, other: __typing.Any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return (self.numerator * FullRationalNumber_other.denominator).__gt__(FullRationalNumber_other.numerator * self.denominator)
        except:
            try:
                return (self.__numerator * other.denominator).__gt__(other.numerator * self.__denominator)
            except:
                from .error import compare_error
                compare_error(self, other, ">")

    def __gt__(self, other: __typing.Any) -> bool:
        try:
            return not self.__lt__(other)
        except:
            from .error import compare_error
            compare_error(self, other, ">=")

    def __pos__(self) -> "FullRationalNumber":
        return self

    def __neg__(self) -> "FullRationalNumber":
        return self.__mul__(FullRationalNumber("-1"))

    def __abs__(self) -> "FullRationalNumber":
        return self if self.__numerator >= 0 else -self

    def __int__(self) -> int:
        return int(self.__numerator / self.__denominator)

    def __float__(self) -> float:
        return float(self.__numerator / self.__denominator)

    def __complex__(self) -> complex:
        return complex(float(self.__numerator / self.__denominator))

    def __bool__(self) -> bool:
        return not not self.__numerator

    def __str__(self) -> str:
        if self.__denominator == 1:
            return f"{self.__numerator}"
        else:
            return f"{self.__numerator}/{self.__denominator}"

    def __repr__(self) -> str:
        return f"FullRationalNumber(\'{self.__str__()}\')"

    del __typing
    del __Decimal
    del __overload


class FullRationalComplexNumber(object):
    '''
    完整的复数类
    '''

    import typing as __typing

    def __init__(self, real: __typing.Any = 0, imaginary: __typing.Any = 0) -> None:
        self.__real: FullRationalNumber = FullRationalNumber(real)
        self.__imainary: FullRationalNumber = FullRationalNumber(imaginary)

    @property
    def real(self) -> FullRationalNumber:
        return self.__real

    @property
    def imainary(self) -> FullRationalNumber:
        return self.__imainary

    def __add__(self, other: __typing.Any) -> "FullRationalComplexNumber":
        return FullRationalComplexNumber(self.__real + other.real, self.__imainary + other.imainary) if isinstance(other, FullRationalComplexNumber) else self + FullRationalComplexNumber(other)

    def __iadd__(self, other: __typing.Any) -> "FullRationalNumber":
        return self.__add__(other)

    del __typing


class FullThread(__threading.Thread):
    '''
    更完整的多线程类

    添加了 `__call__` 和 ```stop``` 方法
    '''

    import typing as __typing

    def __init__(
        self,
        group: None = None,
        target: __typing.Callable[..., object] | None = None,
        name: __typing.Optional[str] = None,
        args: __typing.Iterable = (),
        kwargs: __typing.Mapping[str, __typing.Any] | None = {},
        daemon: __typing.Optional[bool] = None,
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def __call__(self) -> None:
        self.start()

    def stop(self) -> None:
        from ctypes import c_long, py_object, pythonapi
        print("stop start")
        pythonapi.PyThreadState_SetAsyncExc(c_long(self.ident), py_object(SystemExit))
        print("stop stop")

    del __typing


del __threading
