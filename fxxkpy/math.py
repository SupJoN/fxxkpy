# coding:utf-8
import types as __types

import sympy as __sympy

from .error import operation_error as __operation_error


# 最大公因数
def GCF(num1: int, num2: int, sort: bool = False):
    # 这个太慢了
    '''
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
        for i in range(1, min_num):
            i = __sympy.prime(i)
            if min_num % i == 0 and max_num % i == 0:
                return i * GCF(min_num // i, max_num // i, sort=True)
        return 1
    '''
    if type(num1) == int and num1 > 0 and type(num2) == int and num2 > 0:
        if sort:
            min_num = num1
            max_num = num2
        else:
            min_num = min(num1, num2)
            max_num = max(num1, num2)
        if min_num == 1 or max_num - min_num == 1:
            return 1
        elif max_num // min_num == max_num / min_num:
            return min_num
        else:
            return GCF(max_num % min_num, min_num, sort=True)
    else:
        __operation_error(num1, num2, 'GCF')


# 最小公倍数
def LCM(num1: int, num2: int, sort: bool = False):
    if type(num1) == int and num1 > 0 and type(num2) == int and num2 > 0:
        return num1 * num2 // GCF(num1, num2, sort=sort)
    else:
        __operation_error(num1, num2, 'LCM')


# 快速排序
def quickly(data: list, parameter: int or __types.NoneType = None) -> list:
    if parameter.__class__ == int:
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
    elif parameter == None:
        original = [] + data  # 不改变原数据
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


# 计算器
def calculator(input_text: str) -> int:
    text = list(input_text)
    finally_ = ''
    for i in range(len(text)):
        if input_text[i] == '^':
            text[i] = '**'
    for i in text:
        finally_ += i
    return eval(finally_)


# 斐波那契数列
def fibonacci_sequence(index: int) -> int:
    return int(__sympy.S('1 / (5 ** 0.5) * (((1 + 5 ** 0.5) / 2) ** ' + str(index) + ' - ((1 - 5 ** 0.5) / 2) ** ' + str(index) + ')'))


# 质数判断
def prime(num: int) -> bool:
    if num > 1:
        prime = True
        for i in range(2, int(__sympy.S(str(num) + ' ** (1 / 2)') + 1)):
            if num % i == 0:
                prime = False
        return prime
    else:
        return False
