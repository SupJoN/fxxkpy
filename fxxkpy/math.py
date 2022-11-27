# coding:utf-8
from typing import Any as __Any
from sys import modules as __modules

# 无穷大
inf: float = float("inf")


# 分解质因数
def PrimeFactorization(number: int) -> dict:
    '''
    分解质因数函数

    只用试2和非1奇数，而且采用了 sympy.S 进行计算，结果准确

    参数：
        number: 要分解质因数的大于等于 2 的整数

    返回值:
        一个字典，键是质因数，值是指数
    '''
    from decimal import Decimal

    if isinstance(number, (int, float, str, Decimal)):
        try:
            Decimal_number: Decimal = Decimal(str(number))
        except:
            raise ValueError(f"cannot be parsed: {repr(number)}")
        if Decimal_number % 1 == 0:
            if Decimal_number >= 2:
                result = {}
                while Decimal_number & 1 == 0:
                    try:
                        result[2] += 1
                    except:
                        result[2] = 1
                    Decimal_number //= 2
                for i in range(3, 2 * Decimal_number + 3, 2):
                    if Decimal_number == 1:
                        break
                    while Decimal_number % i == 0:
                        try:
                            result[i] += 1
                        except:
                            result[i] = 1
                        Decimal_number //= i
                return result
            else:
                raise TypeError(f"unsupported type for prime factorization: int less than 2")
        else:
            raise TypeError(f"cannot be parsed to int: {repr(number)}")
    else:
        raise TypeError(f"unsupported type for prime factorization: {str(number.__class__)[7:len(str(number.__class__)) - 1]}")


# 最大公因数
def GCF(num1: int, num2: int, sort: bool = False) -> int:
    '''
    一个求最大公因数的函数

    通过小学学的辗转相除法递归计算

    参数:
        num1: 第一个正整数
        num2: 第二个正整数
        sort: 默认为 False ，如果 sort 参数为 True ，则默认 num1 为较小数字，num2 为较大数字
    '''
    if isinstance(num1, int) and num1 > 0 and isinstance(num2, int) and num2 > 0:
        if sort:
            min_num = num1
            max_num = num2
        else:
            min_num = min(num1, num2)
            max_num = max(num1, num2)
        if min_num == 1 or max_num - min_num == 1:
            return 1
        elif max_num % min_num == 0:
            return min_num
        else:
            return GCF(max_num % min_num, min_num, sort=True)
    else:
        from .error import operation_error
        operation_error(num1, num2, "GCF")


# 最小公倍数
def LCM(num1: int, num2: int, sort: bool = False) -> int:
    '''
    一个求最小公倍数的函数

    通过两数乘积除以最大公因数进行计算

    参数:
        num1: 第一个正整数
        num2: 第二个正整数
        sort: 默认为 False ，如果 sort 参数为 True ，则默认 num1 为较大数字，num2 为较小数字
    '''
    if isinstance(num1, int) and num1 > 0 and isinstance(num2, int) and num2 > 0:
        return num1 * num2 // GCF(num1, num2, sort=sort)
    else:
        from .error import operation_error
        operation_error(num1, num2, 'LCM')


# 快速排序
def quickly(data: list, parameter: __Any = None) -> list:
    '''
    列表的快速排序函数

    我都不用系列

    参数:
        data: 要排序的列表
        parameter: 默认为 None ，代表参数，为 None 时默认没有参数
    '''
    if parameter == None:
        original: list = [] + data  # 不改变原数据
        if len(original) > 1:
            standard = original[0]
            del original[0]
            left, right = [], []
            for i in original:
                if i >= standard:
                    right.append(i)
                else:
                    left.append(i)
            return quickly(left) + [standard] + quickly(right)
        else:
            return original
    else:
        original = [] + data  # 不改变原数据
        if len(original) > 1:
            standard = original[0]
            del original[0]
            left, right = [], []
            for i in original:
                if i[parameter] >= standard[parameter]:
                    right.append(i)
                else:
                    left.append(i)
            return quickly(left, parameter) + [standard] + quickly(right, parameter)
        else:
            return original


'''
# 计算器
def calculator(input_text: str) -> float:
    text = list(input_text)
    finally_ = ""
    for i in range(len(text)):
        if input_text[i] == "^":
            text[i] = "**"
    for i in text:
        finally_ += i
    return eval(finally_)
'''

try:
    import sympy as __sympy

    # 斐波那契数列
    def fibonacci_sequence(index: int) -> __sympy.core.Integer:
        return __sympy.core.Integer(__sympy.S(f"1 / (5 ** 0.5) * (((1 + 5 ** 0.5) / 2) ** {index} - ((1 - 5 ** 0.5) / 2) ** {index})"))
except:
    import decimal as __decimal

    # 斐波那契数列
    def fibonacci_sequence(index: int) -> __decimal.Decimal:
        a = b = __decimal.Decimal("1")
        for i in range(index - 1):
            a, b = b, a + b
        return a


# 质数判断
def prime(num: int) -> bool:
    if num > 1:
        prime = True
        for i in range(2, num):
            if i ** 2 > num:
                if num % i == 0:
                    prime = False
            else:
                break
        return prime
    else:
        return False


# 字符串是否是整数形式
def isInt(value: str) -> bool:
    if len(value) >= 1:
        data: str = value[1::] if value[0] in ("+", "-") else value
        return data.isdigit()
    else:
        return False


# 字符串是否是小数形式
def isFloat(value: str) -> bool:
    if len(value) >= 1:
        data: str = value[1::] if value[0] in ("+", "-") else value
        if len(data) >= 1:
            index = data.find(".")
            if index == -1:
                return data.isdigit()
            else:
                return (data[:index:] + data[index + 1::]).isdigit()
        else:
            return False
    else:
        return False


del __Any
