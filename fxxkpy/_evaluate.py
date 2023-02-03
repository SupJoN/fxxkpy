#coding:utf-8
import decimal
import fractions

from .FullBaseObject import *
from .mathematics import isFloat

try:
    import fraction
    isFraction = True
except Exception:
    isFraction = False
try:
    import sympy
    isSympy = True
except Exception:
    isSympy = False

rational_evaluate_type = int | float | str | FullRationalNumber | decimal.Decimal | fractions.Fraction | fraction.Fraction | sympy.core.numbers.Zero | sympy.core.numbers.One | sympy.core.numbers.Integer | sympy.core.numbers.Float

complex_evaluate_type = int | float | complex | str | FullRationalNumber | FullRationalComplexNumber | decimal.Decimal | fractions.Fraction | fraction.Fraction | sympy.core.numbers.Zero | sympy.core.numbers.One | sympy.core.numbers.Integer | sympy.core.numbers.Float


def rational_evaluate(parameter: rational_evaluate_type, name: str) -> tuple[decimal.Decimal, decimal.Decimal]:
    def str_evaluate(parameter: str) -> tuple[decimal.Decimal, decimal.Decimal] | None:
        line: int = parameter.find("/")
        if line == -1:
            if isFloat(parameter):
                return (decimal.Decimal(parameter), decimal.Decimal("1"))
            else:
                return None
        else:
            numerator: str = parameter[:line:]
            denominator: str = parameter[line + 1::]
            if isFloat(numerator) and isFloat(denominator):
                return (decimal.Decimal(numerator), decimal.Decimal(denominator))
            else:
                return None

    isChanged: bool = False
    if isinstance(parameter, int):
        numerator: decimal.Decimal = decimal.Decimal(str(parameter))
        denominator: decimal.Decimal = decimal.Decimal(1)
        isChanged: bool = True
    elif isinstance(parameter, float):
        numerator: decimal.Decimal = decimal.Decimal(str(parameter))
        denominator: decimal.Decimal = decimal.Decimal(1)
        isChanged: bool = True
    elif isinstance(parameter, str):
        if (result := str_evaluate(parameter)):
            numerator: decimal.Decimal = result[0]
            denominator: decimal.Decimal = result[1]
            if denominator == 0:
                raise ZeroDivisionError("division by zero")
            else:
                isChanged: bool = True
        else:
            raise ValueError(f"cannot be evaluated: {repr(parameter)}")
    elif isinstance(parameter, FullRationalNumber):
        numerator: decimal.Decimal = parameter.numerator
        denominator: decimal.Decimal = parameter.denominator
        isChanged: bool = True
    elif isinstance(parameter, decimal.Decimal):
        numerator: decimal.Decimal = parameter
        denominator: decimal.Decimal = decimal.Decimal("1")
        isChanged: bool = True
    elif isinstance(parameter, fractions.Fraction):
        numerator: decimal.Decimal = decimal.Decimal(str(parameter.numerator))
        denominator: decimal.Decimal = decimal.Decimal(str(parameter.denominator))
        isChanged: bool = True
    if not isChanged and isFraction and isinstance(parameter, fraction.Fraction):
        numerator: decimal.Decimal = decimal.Decimal(str(parameter.numerator))
        denominator: decimal.Decimal = decimal.Decimal(str(parameter.denominator))
        isChanged: bool = True
    if not isChanged and isSympy:
        if isinstance(parameter, sympy.core.numbers.Zero):
            numerator: decimal.Decimal = decimal.Decimal("0")
            denominator: decimal.Decimal = decimal.Decimal("1")
            isChanged: bool = True
        elif isinstance(parameter, sympy.core.numbers.One):
            numerator: decimal.Decimal = decimal.Decimal("1")
            denominator: decimal.Decimal = decimal.Decimal("1")
            isChanged: bool = True
        elif isinstance(parameter, sympy.core.numbers.Integer):
            numerator: decimal.Decimal = decimal.Decimal(str(parameter))
            denominator: decimal.Decimal = decimal.Decimal("1")
            isChanged: bool = True
        elif isinstance(parameter, sympy.core.numbers.Float):
            numerator: decimal.Decimal = decimal.Decimal(str(parameter))
            denominator: decimal.Decimal = decimal.Decimal("1")
            isChanged: bool = True
    if not isChanged:
        try:
            numerator: decimal.Decimal = decimal.Decimal(str(parameter.numerator))
            denominator: decimal.Decimal = decimal.Decimal(str(parameter.denominator))
            isChanged: bool = True
        except Exception:
            pass
    if not isChanged:
        try:
            int_parameter: int = int(parameter)
            if int_parameter == parameter:
                numerator: decimal.Decimal = decimal.Decimal(str(int_parameter))
                denominator: decimal.Decimal = decimal.Decimal("1")
                isChanged: bool = True
        except Exception:
            pass
    if not isChanged:
        try:
            int_parameter: float = float(parameter)
            if int_parameter == parameter:
                numerator: decimal.Decimal = decimal.Decimal(str(int_parameter))
                denominator: decimal.Decimal = decimal.Decimal("1")
                isChanged = True
        except Exception:
            pass
    if not isChanged:
        try:
            result: tuple[decimal.Decimal] | None = str_evaluate(str(parameter))
            if result:
                numerator: decimal.Decimal = result[0]
                denominator: decimal.Decimal = result[1]
                isChanged: bool = denominator != 0
        except Exception:
            pass
    if not isChanged:
        try:
            result: tuple[decimal.Decimal, decimal.Decimal] | None = str_evaluate(repr(parameter))
            if result:
                numerator: decimal.Decimal = result[0]
                denominator: decimal.Decimal = result[1]
                isChanged: bool = denominator != 0
        except Exception:
            pass
    if not isChanged:
        raise TypeError(f"{name} doesn't accept arguments of {str(parameter.__class__)[7:len(str(parameter.__class__)) - 1]} when it's initialized")
    return numerator, denominator


def complex_evaluate(parameter: complex_evaluate_type, name: str, i: bool = True, j: bool = True) -> tuple[FullRationalNumber, FullRationalNumber]:
    def str_evaluate(parameter: str) -> tuple[FullRationalNumber, FullRationalNumber] | None:
        if (parameter.count("j") > 1 if j else parameter.find("j") != -1) or (parameter.count("i") > 1 if i else parameter.find("i") != -1):
            raise ValueError(f"cannot be evaluated: {repr(parameter)}")
        else:
            ...

    isChanged: bool = False
    if isinstance(parameter, str):
        ...
