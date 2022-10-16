# coding:utf-8
# 完整的字典
class FullDict(object):
    """
    FullDict
    ========

    可以遍历的默认字典

    使用 self.__index 保存列表的所有已知 (经过赋值的) 键

    属性:
        __default: 默认值
        __clear: 是否启用 ```clear``` 方法, 默认为 ```False```
        __fdict: 存放 ```defaultdict``` 的属性
        __index: 保存列表的所有已知(经过赋值的)键
        __KeyIterator: 存放 ```FullDictKeyIterator``` 类的属性
    """
    __slots__: tuple = ("__default", "__clear", "__fdict", "__index", "__KeyIterator")

    def __init__(self, *args: any, **kwargs: any) -> None:
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

    @default.setter
    def default(self, value: any) -> None:
        self.__default: any = value

    @property
    def fdict(self) -> any:
        return self.__fdict

    def clear(self) -> None:
        if self.__clear:
            self.__fdict.clear()
            self.__index: list = []
        else:
            raise AttributeError("'FullDict' object has no attribute 'clear'")

    def get(self, key: any, default: any = None) -> any:
        return self[key] if key in self.__index else default

    def setdefault(self, key, default: any = None) -> any:
        self[key] = self[key] if key in self.__index else default
        return self[key]

    def pop(self, key: any, default: any = ...) -> any:
        if type(default) == Ellipsis:
            try:
                result = self[key]
                del self[key]
                return result
            except:
                raise KeyError(repr(key))
        else:
            try:
                result = self[key]
                del self[key]
                return result
            except:
                return default

    def popitem(self) -> tuple:
        if len(self.__index) != 0:
            result = self.__index[-1], self[self.__index[-1]]
            del self[self.__index[-1]]
            return result
        else:
            raise KeyError("popitem(): dictionary is empty")

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
        if key not in self.__index:
            self.__index.append(key)
        self.__fdict.__setitem__(key, value)

    def __delitem__(self, key: any) -> None:
        if key in self.__index:
            self.__index.remove(key)
            self.__fdict.__delitem__(key)
        else:
            raise KeyError(repr(key))

    def __bool__(self) -> bool:
        return bool(self.__index)

    def __eq__(self, other: any) -> bool:
        if type(other) == FullDict:
            return other.fdict == self.fdict
        else:
            return False

    def __ne__(self, other: any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> "FullDict.__KeyIterator":
        return self.__KeyIterator(self.__index)

    def __repr__(self) -> str:
        return f"FullDict({self.__default}{self.__fdict.__repr__()[79:len(self.__fdict.__repr__())]}"

    def __str__(self) -> str:
        return self.__repr__()


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

    from decimal import Decimal as __Decimal
    from typing import overload as __overload

    @__overload
    def __init__(self) -> None:
        ...

    @__overload
    def __init__(self, numerator: any, denominator: any) -> None:
        ...

    @__overload
    def __init__(self, value: any) -> None:
        ...

    def __init__(self, *args: any) -> None:
        import decimal

        try:
            import fraction
            isFraction = True
        except:
            isFraction = False
        try:
            import fractions
            isFractions = True
        except:
            isFractions = False
        try:
            import sympy
            isSympy = True
        except:
            isSympy = False

        if len(args) == 0:
            self.__numerator = decimal.Decimal("0")
            self.__denominator = decimal.Decimal("1")
            return
        elif len(args) == 1:
            isChanged = False
            if type(args[0]) == int:
                self.__numerator = decimal.Decimal(str(args[0]))
                self.__denominator = decimal.Decimal(1)
                return
            elif type(args[0]) == float:
                self.__numerator = decimal.Decimal(str(args[0]))
                self.__denominator = decimal.Decimal(1)
                isChanged = True
            elif type(args[0]) == str:
                try:
                    line = args[0].index("/")
                    self.__numerator = decimal.Decimal(args[0][:line:])
                    self.__denominator = decimal.Decimal(args[0][line + 1::])
                    if self.__denominator == 0:
                        raise ZeroDivisionError("division by zero")
                    else:
                        isChanged = True
                except ValueError:
                    try:
                        self.__numerator = decimal.Decimal(args[0])
                        self.__denominator = 1
                        isChanged = True
                    except decimal.InvalidOperation:
                        raise ValueError(f"cannot be parsed: {repr(args[0])}")
                except decimal.InvalidOperation:
                    raise ValueError(f"cannot be parsed: {repr(args[0])}")
            elif type(args[0]) == FullRationalNumber:
                self.__numerator = args[0].numerator
                self.__denominator = args[0].denominator
                return
            elif type(args[0]) == decimal.Decimal:
                self.__numerator = args[0]
                self.__denominator = decimal.Decimal("1")
                isChanged = True
            if not isChanged and isFraction:
                if type(args[0]) == fraction.Fraction:
                    self.__numerator = decimal.Decimal(str(args[0].numerator))
                    self.__denominator = decimal.Decimal(str(args[0].denominator))
                    isChanged = True
            if not isChanged and isFractions:
                if type(args[0]) == fractions.Fraction:
                    self.__numerator = decimal.Decimal(str(args[0].numerator))
                    self.__denominator = decimal.Decimal(str(args[0].denominator))
                    isChanged = True
            if not isChanged and isSympy:
                if type(args[0]) == sympy.core.numbers.Zero:
                    self.__numerator = decimal.Decimal("0")
                    self.__denominator = decimal.Decimal("1")
                    return
                elif type(args[0]) == sympy.core.numbers.One:
                    self.__numerator = decimal.Decimal("1")
                    self.__denominator = decimal.Decimal("1")
                    return
                elif type(args[0]) == sympy.core.numbers.Integer:
                    self.__numerator = decimal.Decimal(str(args[0]))
                    self.__denominator = decimal.Decimal("1")
                    return
                elif type(args[0]) == sympy.core.numbers.Float:
                    self.__numerator = decimal.Decimal(str(args[0]))
                    self.__denominator = decimal.Decimal("1")
                    isChanged = True
            if not isChanged:
                raise TypeError(f"FullRationalNumber doesn't accept arguments of {str(args[0].__class__)[7:len(str(args[0].__class__)) - 1]} when it's initialized")
        elif len(args) == 2:
            isChanged = False
            if type(args[1]) == str:
                try:
                    is0 = float(args[1]) == 0
                except:
                    is0 = False
            else:
                is0 = args[1] == 0
            if not is0:
                self.__numerator = decimal.Decimal("1")
                self.__denominator = decimal.Decimal("1")
                if type(args[0]) in (int, float):
                    self.__numerator *= decimal.Decimal(str(args[0]))
                    isChanged = True
                elif type(args[0]) == str:
                    try:
                        line = args[0].index("/")
                        self.__numerator *= decimal.Decimal(args[0][:line:])
                        self.__denominator *= decimal.Decimal(args[0][line + 1::])
                        if self.__denominator == 0:
                            raise ZeroDivisionError("division by zero")
                        else:
                            isChanged = True
                    except ValueError:
                        try:
                            self.__numerator *= decimal.Decimal(args[0])
                            self.__denominator *= 1
                            isChanged = True
                        except decimal.InvalidOperation:
                            raise ValueError(f"cannot be parsed: {repr(args[0])}")
                    except decimal.InvalidOperation:
                        raise ValueError(f"cannot be parsed: {repr(args[0])}")
                elif type(args[0]) == decimal.Decimal:
                    self.__numerator *= args[0]
                    isChanged = True
                elif type(args[0]) == FullRationalNumber:
                    self.__numerator *= args[0].numerator
                    self.__denominator *= args[0].denominator
                    isChanged = True
                elif type(args[0]) == decimal.Decimal:
                    self.__numerator *= args[0]
                    isChanged = True
                if not isChanged and isFraction:
                    if type(args[0]) == fraction.Fraction:
                        self.__numerator *= decimal.Decimal(str(args[0].numerator))
                        self.__denominator *= decimal.Decimal(str(args[0].denominator))
                        isChanged = True
                if not isChanged and isFractions:
                    if type(args[0]) == fractions.Fraction:
                        self.__numerator *= decimal.Decimal(str(args[0].numerator))
                        self.__denominator *= decimal.Decimal(str(args[0].denominator))
                        isChanged = True
                if not isChanged and isSympy:
                    if type(args[0]) == sympy.core.numbers.Zero:
                        self.__numerator *= decimal.Decimal("0")
                        self.__denominator *= decimal.Decimal("1")
                        return
                    elif type(args[0]) == sympy.core.numbers.One:
                        isChanged = True
                    elif type(args[0]) == sympy.core.numbers.Integer:
                        self.__numerator *= decimal.Decimal(str(args[0]))
                        isChanged = True
                    elif type(args[0]) == sympy.core.numbers.Float:
                        self.__numerator *= decimal.Decimal(str(args[0]))
                        isChanged = True
                if not isChanged:
                    raise TypeError(f"FullRationalNumber's numerator doesn't accept arguments of {str(args[0].__class__)[7:len(str(args[0].__class__)) - 1]} when it's initialized")

                isChanged = False
                if type(args[1]) in (int, float):
                    self.__denominator *= decimal.Decimal(str(args[1]))
                    isChanged = True
                elif type(args[1]) == str:
                    try:
                        line = args[0].index("/")
                        self.__denominator *= decimal.Decimal(args[1][:line:])
                        self.__numerator *= decimal.Decimal(args[1][line + 1::])
                        if self.__denominator == 0:
                            raise ZeroDivisionError("division by zero")
                        else:
                            isChanged = True
                    except ValueError:
                        try:
                            self.__denominator *= decimal.Decimal(args[1])
                            self.__numerator *= 1
                            isChanged = True
                        except decimal.InvalidOperation:
                            raise ValueError(f"cannot be parsed: {repr(args[1])}")
                    except decimal.InvalidOperation:
                        raise ValueError(f"cannot be parsed: {repr(args[1])}")
                elif type(args[1]) == decimal.Decimal:
                    self.__denominator *= args[1]
                    isChanged = True
                elif type(args[1]) == FullRationalNumber:
                    self.__denominator *= args[1].numerator
                    self.__numerator *= args[1].denominator
                    isChanged = True
                elif type(args[1]) == decimal.Decimal:
                    self.__denominator *= args[1]
                    isChanged = True
                if not isChanged and isFraction:
                    if type(args[1]) == fraction.Fraction:
                        self.__denominator *= decimal.Decimal(str(args[1].numerator))
                        self.__numerator *= decimal.Decimal(str(args[1].denominator))
                        isChanged = True
                if not isChanged and isFractions:
                    if type(args[1]) == fractions.Fraction:
                        self.__denominator *= decimal.Decimal(str(args[1].numerator))
                        self.__numerator *= decimal.Decimal(str(args[1].denominator))
                        isChanged = True
                if not isChanged and isSympy:
                    if type(args[1]) == sympy.core.numbers.One:
                        self.__denominator *= decimal.Decimal("1")
                        self.__numerator *= decimal.Decimal("1")
                        isChanged = True
                    elif type(args[1]) == sympy.core.numbers.Integer:
                        self.__denominator *= decimal.Decimal(str(args[1]))
                        isChanged = True
                    elif type(args[1]) == sympy.core.numbers.Float:
                        self.__denominator *= decimal.Decimal(str(args[1]))
                        isChanged = True
                if not isChanged:
                    raise TypeError(f"FullRationalNumber's denominator doesn't accept arguments of {str(args[1].__class__)[7:len(str(args[1].__class__)) - 1]} when it's initialized")
            else:
                raise ZeroDivisionError("division by zero")
        else:
            raise TypeError(f"FullRationalNumber.__init__() takes from 0 to 2 positional arguments but {len(args)} were given")

        while self.__numerator % 1 != 0 or self.__denominator % 1 != 0:
            self.__numerator *= 10
            self.__denominator *= 10

        try:
            self.__numerator = decimal.Decimal(str(self.__numerator)[:str(self.__numerator).index("."):])
        except:
            pass

        try:
            self.__denominator = decimal.Decimal(str(self.__denominator)[:str(self.__denominator).index("."):])
        except:
            pass

        if min(abs(self.__numerator), abs(self.__denominator)) >= 2:
            for i in range(2, int(min(abs(self.__numerator), abs(self.__denominator)) + 1)):
                while self.__numerator % i == 0 and self.__denominator % i == 0:
                    self.__numerator //= i
                    self.__denominator //= i

        if self.__denominator < 0:
            self.__numerator = -self.__numerator
            self.__denominator = -self.__denominator

    def simplification(self) -> None:
        import decimal

        if self.__numerator == 0:
            self.__denominator = 1
            return
        else:
            while self.__numerator != int(self.__numerator) or self.__denominator != int(self.__denominator):
                self.__numerator *= 10
                self.__denominator *= 10

            try:
                self.__numerator = decimal.Decimal(str(self.__numerator)[:str(self.__numerator).index("."):])
            except:
                pass

            try:
                self.__denominator = decimal.Decimal(str(self.__denominator)[:str(self.__denominator).index("."):])
            except:
                pass

            if min(abs(self.__numerator), abs(self.__denominator)) >= 2:
                for i in range(2, int(min(abs(self.__numerator), abs(self.__denominator)) + 1)):
                    while self.__numerator % i == 0 and self.__denominator % i == 0:
                        self.__numerator //= i
                        self.__denominator //= i

            if self.__denominator < 0:
                self.__numerator = -self.__numerator
                self.__denominator = -self.__denominator

    def clear(self) -> None:
        import decimal

        self.__numerator = decimal.Decimal("0")
        self.__denominator = decimal.Decimal("1")

    @property
    def numerator(self) -> __Decimal:
        return self.__numerator

    @property
    def denominator(self) -> __Decimal:
        return self.__denominator

    def __add__(self, other: any) -> "FullRationalNumber":
        if type(other) == FullRationalNumber:
            return FullRationalNumber(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)
        else:
            return self + FullRationalNumber(other)

    def __radd__(self, other: any) -> "FullRationalNumber":
        return self + FullRationalNumber(other)

    def __iadd__(self, other: any) -> "FullRationalNumber":
        return self + FullRationalNumber(other)

    def __sub__(self, other: any) -> "FullRationalNumber":
        FullRationalNumber_other = FullRationalNumber(other)
        return self + -FullRationalNumber_other

    def __rsub__(self, other: any) -> "FullRationalNumber":
        FullRationalNumber_other = FullRationalNumber(other)
        return FullRationalNumber_other + -self

    def __isub__(self, other: any) -> "FullRationalNumber":
        return self - other

    def __mul__(self, other: any) -> "FullRationalNumber":
        if type(other) == FullRationalNumber:
            result = FullRationalNumber(self.numerator * other.numerator, self.denominator * other.denominator)
            return result
        else:
            return self * FullRationalNumber(other)

    def __rmul__(self, other: any) -> "FullRationalNumber":
        return self * other

    def __imul__(self, other: any) -> "FullRationalNumber":
        return self * other

    def __truediv__(self, other: any) -> "FullRationalNumber":
        inverse = FullRationalNumber(other)
        if inverse.numerator != 0:
            inverse = FullRationalNumber(inverse.denominator, inverse.numerator)
            return self * inverse
        else:
            raise ZeroDivisionError("division by zero")

    def __rtruediv__(self, other: any) -> "FullRationalNumber":
        if self.numerator != 0:
            inverse = FullRationalNumber(self.__denominator, self.__numerator)
            return other * inverse
        else:
            raise ZeroDivisionError("division by zero")

    def __itruediv__(self, other: any) -> "FullRationalNumber":
        return self / other

    def __pow__(self, other: any) -> "FullRationalNumber":
        FullRationalNumber_other = FullRationalNumber(other)
        if FullRationalNumber_other.denominator == 1:
            if FullRationalNumber_other.numerator > 0:
                result = FullRationalNumber("1")
                for i in range(int(FullRationalNumber_other.numerator)):
                    result *= self
                return result
            elif FullRationalNumber_other.numerator == 0:
                if self.numerator == 0:
                    raise ZeroDivisionError("division by zero")
                else:
                    return FullRationalNumber("1")
            else:
                return 1 / (self ** -FullRationalNumber_other.numerator)
        else:
            raise TypeError(f"unsupported operand value for \'**\': {repr(self)} and {repr(other)} whose denominator isn't 1")

    def __rpow__(self, other: any) -> "FullRationalNumber":
        if self.denominator == 1:
            FullRationalNumber_other = FullRationalNumber(other)
            if self.numerator > 0:
                result = FullRationalNumber("1")
                for i in range(int(self.numerator)):
                    result *= self
                return result
            elif self.numerator == 0:
                if FullRationalNumber_other.numerator == 0:
                    raise ZeroDivisionError("division by zero")
                else:
                    return FullRationalNumber("1")
            else:
                return 1 / (FullRationalNumber_other ** -self.numerator)
        else:
            raise TypeError(f"unsupported operand value for \'**\': {repr(other)} and {repr(self)} whose denominator isn't 1")

    def __ipow__(self, other: any) -> "FullRationalNumber":
        FullRationalNumber_other = FullRationalNumber(other)
        try:
            return self ** FullRationalNumber_other
        except TypeError:
            raise TypeError(f"unsupported operand value for \'**=\': {repr(self)} and {repr(other)} whose denominator isn't 1")

    def __lt__(self, other: any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return self.numerator * FullRationalNumber_other.denominator < FullRationalNumber_other.numerator * self.denominator
        except:
            try:
                return other > float(self)
            except:
                from .error import compare_error
                compare_error(self, other, "<")

    def __le__(self, other: any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return self.numerator * FullRationalNumber_other.denominator <= FullRationalNumber_other.numerator * self.denominator
        except:
            try:
                return other >= float(self)
            except:
                from .error import compare_error
                compare_error(self, other, "<=")

    def __eq__(self, other: any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return self.numerator * FullRationalNumber_other.denominator == FullRationalNumber_other.numerator * self.denominator
        except:
            try:
                return other == float(self)
            except:
                return False

    def __ne__(self, other: any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return self.numerator * FullRationalNumber_other.denominator != FullRationalNumber_other.numerator * self.denominator
        except:
            try:
                return other != float(self)
            except:
                return True

    def __gt__(self, other: any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return self.numerator * FullRationalNumber_other.denominator > FullRationalNumber_other.numerator * self.denominator
        except:
            try:
                return other < float(self)
            except:
                from .error import compare_error
                compare_error(self, other, ">")

    def __gt__(self, other: any) -> bool:
        try:
            FullRationalNumber_other = FullRationalNumber(other)
            return self.numerator * FullRationalNumber_other.denominator >= FullRationalNumber_other.numerator * self.denominator
        except:
            try:
                return other <= float(self)
            except:
                from .error import compare_error
                compare_error(self, other, ">=")

    def __pos__(self) -> "FullRationalNumber":
        return self

    def __neg__(self) -> "FullRationalNumber":
        return self * -1

    def __abs__(self) -> "FullRationalNumber":
        return self if self.numerator >= 0 else -self

    def __int__(self) -> int:
        return int(self.numerator / self.denominator)

    def __float__(self) -> float:
        return float(self.__numerator / self.__denominator)

    def __bool__(self) -> bool:
        return self.__numerator != 0

    def __str__(self) -> str:
        if self.__denominator == 1:
            return f"{self.__numerator}"
        else:
            return f"{self.__numerator}/{self.__denominator}"

    def __repr__(self) -> str:
        return f"FullRationalNumber(\'{self.__str__()}\')"
