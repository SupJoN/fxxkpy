# coding:utf-8
from threading import Thread as _Thread
from decimal import getcontext as _getcontext

_getcontext().prec = 64


class _Number(object):
    '''
    数字
    '''

    __slots__: tuple[str, ...] = ()

    _Prec: type = type("_Prec", (int, ), {})
    __short: _Prec = _Prec(32)
    __middle: _Prec = _Prec(64)
    __long: _Prec = _Prec(128)
    __longlong: _Prec = _Prec(256)

    @property
    def default(self) -> _Prec:
        return self.__middle

    @property
    def short(self) -> _Prec:
        return self.__short

    @property
    def middle(self) -> _Prec:
        return self.__middle

    @property
    def long(self) -> _Prec:
        return self.__long

    @property
    def longlong(self) -> _Prec:
        return self.__longlong

    @property
    def prec(self) -> int:
        '''
        `decimal.Decimal` 的长度
        '''
        from decimal import getcontext as _getcontext
        return _getcontext().prec

    @prec.setter
    def prec(self, value: int) -> None:
        from decimal import getcontext as _getcontext
        _getcontext().prec: int = value


number: _Number = _Number()


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

    import typing as _typing

    __slots__: tuple[str, ...] = ("__default", "__clear", "__fdict", "__index")

    class KeyIterator(object):
        import typing as _typing

        __slots__: tuple[str, ...] = ("index", "current")

        def __init__(self, index: list) -> None:
            self.index: list = index
            self.current: int = 0

        def __next__(self) -> _typing.Any:
            import typing as _typing

            if self.current < len(self.index):
                item: _typing.Any = self.index[self.current]
                self.current += 1
                return item
            else:
                raise StopIteration

        def __iter__(self) -> "FullDict.__KeyIterator":
            return self

    def __init__(self, *args: _typing.Any, **kwargs: _typing.Any) -> None:
        from collections import defaultdict

        length: int = len(args)
        if length:
            if length - 1:
                self.__default: tuple = args
            else:
                import typing as _typing
                self.__default: _typing.Any = args[0]
        else:
            self.__default: None = None
        self.__fdict: defaultdict = defaultdict(lambda: self.__default)

        try:
            if kwargs["clear"] == True:
                self.__clear: bool = True
            else:
                self.__clear: bool = False
        except Exception:
            self.__clear: bool = False

        self.__index: list = []

    @property
    def default(self) -> _typing.Any:
        return self.__default

    @default.setter
    def default(self, value: _typing.Any) -> None:
        import typing
        self.__default: typing.Any = value

    @property
    def fdict(self) -> _typing.Any:
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
    def fromkeys(seq: _typing.Iterable, default: _typing.Any) -> "FullDict":
        result: FullDict = FullDict(default)
        for i in seq:
            result[i] = default
        return result

    def get(self, key: _typing.Any, default: _typing.Any = None) -> _typing.Any:
        return self[key] if key in self.__index else default

    def setdefault(self, key, default: _typing.Any = None) -> _typing.Any:
        import typing
        self[key]: typing.Any = self[key] if key in self.__index else default
        return self[key]

    @_typing.overload
    def pop(self, key: _typing.Any) -> _typing.Any:
        ...

    @_typing.overload
    def pop(self, key: _typing.Any, default: _typing.Any) -> _typing.Any:
        ...

    def pop(self, *args: _typing.Any, **kwargs: _typing) -> _typing.Any:
        import typing as _typing

        def key_pop(key: _typing.Any) -> _typing.Any:
            if args[0] not in self.__index:
                raise KeyError(repr(key))
            else:
                import typing
                result: typing.Any = self[key]
                del self[key]
                return result

        def default_pop(key: _typing.Any, default: _typing.Any) -> _typing.Any:
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

    def popitem(self) -> tuple[_typing.Any, _typing.Any]:
        if len(self.__index) != 0:
            result = self.__index[-1], self[self.__index[-1]]
            del self[self.__index[-1]]
            return result
        else:
            raise KeyError("popitem(): dictionary is empty")

    def items(self) -> list[tuple[_typing.Any, _typing.Any]]:
        import typing
        result: list[tuple[typing.Any, typing.Any]] = []
        for i in self.__index:
            result.append((i, self.__fdict[i]))
        return result

    def keys(self) -> list[_typing.Any]:
        return self.__index

    def values(self) -> list[_typing.Any]:
        import typing
        result: list[typing.Any] = []
        for i in self.__index:
            result.append(self.__fdict[i])
        return result

    def __len__(self) -> int:
        return len(self.__index)

    def __contains__(self, item: _typing.Any) -> bool:
        return item in self.__index

    def __getitem__(self, key: _typing.Any) -> _typing.Any:
        return self.__fdict.__getitem__(key)

    def __setitem__(self, key: _typing.Any, value: _typing.Any) -> None:
        if key not in self.__index:
            self.__index.append(key)
        self.__fdict.__setitem__(key, value)

    def __delitem__(self, key: _typing.Any) -> None:
        if key in self.__index:
            self.__index.remove(key)
            self.__fdict.__delitem__(key)
        else:
            raise KeyError(repr(key))

    def __bool__(self) -> bool:
        return not not self.__index

    def __eq__(self, other: _typing.Any) -> bool:
        if isinstance(other, FullDict):
            return other._FullDict__fdict == self.__fdict
        else:
            return False

    def __ne__(self, other: _typing.Any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> "FullDict.KeyIterator":
        return self.KeyIterator(self.__index)

    def __repr__(self) -> str:
        fdict_str: str = self.__fdict.__repr__()
        return f"FullDict({self.__default}{fdict_str[fdict_str.index('>, ')+1::]})"

    def __str__(self) -> str:
        return self.__repr__()

    del _typing


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

    import typing as _typing
    from decimal import Decimal as _Decimal

    __slots__: tuple[str, ...] = ("__numerator", "__denominator")

    @_typing.overload
    def __init__(self) -> None:
        ...

    @_typing.overload
    def __init__(self, numerator: _typing.Any, denominator: _typing.Any) -> None:
        ...

    @_typing.overload
    def __init__(self, value: _typing.Any) -> None:
        ...

    def __init__(self, *args: _typing.Any) -> None:
        import decimal

        from ._evaluate import rational_evaluate

        print(f"{decimal.getcontext().prec=}")

        if len(args) == 0:
            self.__numerator: decimal.Decimal = decimal.Decimal("0")
            self.__denominator: decimal.Decimal = decimal.Decimal("1")
            return
        elif len(args) == 1:
            self.__numerator, self.__denominator = rational_evaluate(args[0], "FullRationalNumber")
        elif len(args) == 2:
            self.__numerator, self.__denominator = rational_evaluate(args[0], "FullRationalNumber")
            result = rational_evaluate(args[1], "FullRationalNumber")
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
        except Exception:
            pass

        try:
            self.__denominator: decimal.Decimal = decimal.Decimal(str(self.__denominator)[:str(self.__denominator).index("."):])
        except Exception:
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
            except Exception:
                pass

            try:
                self.__denominator: decimal.Decimal = decimal.Decimal(str(self.__denominator)[:str(self.__denominator).index("."):])
            except Exception:
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
    def numerator(self) -> _Decimal:
        return self.__numerator

    @property
    def denominator(self) -> _Decimal:
        return self.__denominator

    def __add__(self, other: _typing.Any) -> "FullRationalNumber":
        if isinstance(other, FullRationalNumber):
            return FullRationalNumber(self.__numerator * other.denominator + other.numerator * self.__denominator, self.__denominator * other.denominator)
        else:
            return self.__add__(FullRationalNumber(other))

    def __radd__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__add__(FullRationalNumber(other))

    def __iadd__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__add__(FullRationalNumber(other))

    def __sub__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__add__(-FullRationalNumber(other))

    def __rsub__(self, other: _typing.Any) -> "FullRationalNumber":
        return FullRationalNumber(other).__add__(-self)

    def __isub__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__sub__(FullRationalNumber(other))

    def __mul__(self, other: _typing.Any) -> "FullRationalNumber":
        if isinstance(other, FullRationalNumber):
            return FullRationalNumber(self.__numerator * other.numerator, self.__denominator * other.denominator)
        else:
            return self.__mul__(FullRationalNumber(other))

    def __rmul__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__mul__(FullRationalNumber(other))

    def __imul__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__mul__(FullRationalNumber(other))

    def __truediv__(self, other: _typing.Any) -> "FullRationalNumber":
        inverse: FullRationalNumber = FullRationalNumber(other)
        if inverse.numerator != 0:
            return self.__mul__(FullRationalNumber(inverse.denominator, inverse.numerator))
        else:
            raise ZeroDivisionError("division by zero")

    def __rtruediv__(self, other: _typing.Any) -> "FullRationalNumber":
        if self.__numerator != 0:
            return FullRationalNumber(other).__mul__(FullRationalNumber(self.__denominator, self.__numerator))
        else:
            raise ZeroDivisionError("division by zero")

    def __itruediv__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__truediv__(FullRationalNumber(other))

    def __pow__(self, other: _typing.Any) -> "FullRationalNumber":
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

    def __rpow__(self, other: _typing.Any) -> "FullRationalNumber":
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

    def __ipow__(self, other: _typing.Any) -> "FullRationalNumber":
        FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
        try:
            return self.__pow__(FullRationalNumber_other)
        except TypeError:
            raise TypeError(f"unsupported operand value for \'**=\': {repr(self)} and {repr(other)} whose denominator isn't 1")

    def __lt__(self, other: _typing.Any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return (self.numerator * FullRationalNumber_other.denominator).__lt__(FullRationalNumber_other.numerator * self.denominator)
        except Exception:
            try:
                return (self.__numerator * other.denominator).__lt__(other.numerator * self.__denominator)
            except Exception:
                from .error import compare_error
                compare_error(self, other, "<")

    def __le__(self, other: _typing.Any) -> bool:
        try:
            return not self.__gt__(other)
        except Exception:
            from .error import compare_error
            compare_error(self, other, "<=")

    def __eq__(self, other: _typing.Any) -> bool:
        try:
            FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
            return (self.__numerator * FullRationalNumber_other.denominator).__eq__(FullRationalNumber_other.numerator * self.__denominator)
        except Exception:
            try:
                return (self.__numerator * other.denominator).__eq__(other.numerator * self.__denominator)
            except Exception:
                return False

    def __ne__(self, other: _typing.Any) -> bool:
        try:
            FullRationalNumber_other: FullRationalNumber = FullRationalNumber(other)
            return (self.__numerator * FullRationalNumber_other.denominator).__ne__(FullRationalNumber_other.numerator * self.__denominator)
        except Exception:
            return True

    def __gt__(self, other: _typing.Any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return (self.numerator * FullRationalNumber_other.denominator).__gt__(FullRationalNumber_other.numerator * self.denominator)
        except Exception:
            try:
                return (self.__numerator * other.denominator).__gt__(other.numerator * self.__denominator)
            except Exception:
                from .error import compare_error
                compare_error(self, other, ">")

    def __gt__(self, other: _typing.Any) -> bool:
        try:
            return not self.__lt__(other)
        except Exception:
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
        return complex(self.__numerator / self.__denominator)

    def __bool__(self) -> bool:
        return not not self.__numerator

    def __str__(self) -> str:
        if self.__denominator == 1:
            return f"{self.__numerator}"
        else:
            return f"{self.__numerator}/{self.__denominator}"

    def __repr__(self) -> str:
        return f"FullRationalNumber(\'{self.__str__()}\')"

    del _typing
    del _Decimal


class FullRationalComplexNumber(object):
    '''
    FullRationalComplexNumber
    =========================

    完整的复数类
    '''

    import typing as _typing

    __slots__: tuple[str, ...] = ("__real", "__imainary")

    def __init__(self, real: _typing.Any = 0, imaginary: _typing.Any = 0) -> None:
        self.__real: FullRationalNumber = FullRationalNumber(real)
        self.__imainary: FullRationalNumber = FullRationalNumber(imaginary)

    @property
    def real(self) -> FullRationalNumber:
        return self.__real

    @property
    def imainary(self) -> FullRationalNumber:
        return self.__imainary

    def __add__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return FullRationalComplexNumber(self.__real.__add__(other.real), self.__imainary.__add__(other.imainary)) if isinstance(other, FullRationalComplexNumber) else self.__add__(FullRationalComplexNumber(other))

    def __radd__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__add__(other)

    def __iadd__(self, other: _typing.Any) -> "FullRationalNumber":
        return self.__add__(other)

    def __sub__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__add__(FullRationalComplexNumber(other).__neg__())

    def __rsub__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__sub__(other).__neg__()

    def __isub__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__sub__(other)

    def __mul__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return FullRationalComplexNumber(
            self.__real.__mul__(other.real).__sub__(self.__imainary.__mul__(other.imainary)),
            self.__real.__mul__(other.imainary).__add__(self.__imainary.__mul__(other.real)),
        ) if isinstance(other, FullRationalComplexNumber) else self.__mul__(FullRationalComplexNumber(other))

    def __rmul__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__mul__(other)

    def __imul__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__mul__(other)

    def __truediv__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return FullRationalComplexNumber(
            (self.__real.__mul__(other.real).__add__(self.__imainary.__mul__(other.imainary))).__truediv__(other.real.__mul__(other.real).__add__(other.imainary.__mul__(other.imainary))),
            (self.__imainary.__mul__(other.real).__sub__(self.__real.__mul__(other.imainary))).__truediv__(other.real.__mul__(other.real).__add__(other.imainary.__mul__(other.imainary))),
        ) if isinstance(other, FullRationalComplexNumber) else self.__truediv__(FullRationalComplexNumber(other))

    def __rtruediv__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return FullRationalComplexNumber(1).__truediv__(self.__truediv__(other))

    def __itruediv__(self, other: _typing.Any) -> "FullRationalComplexNumber":
        return self.__truediv__(other)

    def __eq__(self, other: _typing.Any) -> bool:
        try:
            return self.__real.__eq__((FullRationalComplexNumber_other := FullRationalComplexNumber(other)).real) and self.__imainary.__eq__(FullRationalComplexNumber_other.imainary)
        except Exception:
            return False

    def __ne__(self, other: _typing.Any) -> bool:
        return not self.__eq__(other)

    def __bool__(self) -> bool:
        return self.__real.__bool__() or self.__imainary.__bool__()

    def __complex__(self) -> complex:
        return complex(self.__real, self.__imainary)

    def __str__(self) -> str:
        return f"{self.__real}+{self.__imainary}i" if self.__imainary.denominator == 1 else f"{self.__real}+{self.__imainary.numerator}j/{self.__imainary.denominator}"

    def __repr__(self) -> str:
        return f"FullRationalComplexNumber({self.__str__()})"

    def __pos__(self) -> "FullRationalComplexNumber":
        return self

    def __neg__(self) -> "FullRationalComplexNumber":
        return FullRationalComplexNumber(self.__real.__neg__, self.__imainary.__neg__)

    def __abs__(self) -> float:
        return self.__complex__().__abs__()

    del _typing


class FullThread(_Thread):
    '''
    FullThread
    ==========

    更完整的多线程类

    添加了 `__call__` 和 ```stop``` 方法
    '''

    import typing as _typing

    def __init__(
        self,
        group: None = None,
        target: _typing.Callable[..., object] | None = None,
        name: str | None = None,
        args: _typing.Iterable = (),
        kwargs: _typing.Mapping[str, _typing.Any] = {},
        daemon: bool | None = None,
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def __call__(self) -> None:
        self.start()

    def stop(self) -> None:
        from ctypes import c_long, py_object, pythonapi
        pythonapi.PyThreadState_SetAsyncExc(c_long(self.ident), py_object(SystemExit))

    del _typing


class FullVersion(object):
    '''
    FullVersion
    ===========

    完整的版本类
    '''

    import typing as _typing

    __slots__: tuple[str, ...] = ("__major", "__minor", "__micro", "__releaselevel", "__serial")

    def __init__(self) -> None:
        import sys
        self.__major: int = sys.version_info.major
        self.__minor: int = sys.version_info.minor
        self.__micro: int = sys.version_info.micro
        self.__releaselevel: str = sys.version_info.releaselevel
        self.__serial: int = sys.version_info.serial

    @property
    def major(self) -> int:
        return self.__major

    @property
    def minor(self) -> int:
        return self.__minor

    @property
    def micro(self) -> int:
        return self.__micro

    @property
    def releaselevel(self) -> str:
        return self.__releaselevel

    @property
    def serial(self) -> int:
        return self.__serial

    def __lt__(self, other: _typing.Iterable[int]) -> bool:
        return (self.__major, self.__minor, self.__micro).__lt__(tuple(other))

    def __le__(self, other: _typing.Iterable[int]) -> bool:
        return (self.__major, self.__minor, self.__micro).__le__(tuple(other))

    def __eq__(self, other: _typing.Iterable[int]) -> bool:
        return (self.__major, self.__minor, self.__micro).__eq__(tuple(other))

    def __ne__(self, other: _typing.Iterable[int]) -> bool:
        return (self.__major, self.__minor, self.__micro).__ne__(tuple(other))

    def __gt__(self, other: _typing.Iterable[int]) -> bool:
        return (self.__major, self.__minor, self.__micro).__gt__(tuple(other))

    def __ge__(self, other: _typing.Iterable[int]) -> bool:
        return (self.__major, self.__minor, self.__micro).__ge__(tuple(other))

    def __iter__(self) -> _typing.Iterator[int]:
        return (self.__major, self.__minor, self.__micro).__iter__()

    def __str__(self) -> str:
        import sys
        return sys.version

    def __repr__(self) -> str:
        return self.__str__()

    del _typing


del _Thread
del _getcontext
