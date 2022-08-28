# coding:utf-8
import sympy as __sympy

from .error import operation_error as __operation_error


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
    if number.__class__ == int:
        if number >= 2:
            result = {}
            num = number
            while __sympy.S(f"{num} // 2") == __sympy.S(f"{num} / 2"):
                try:
                    result[2] += 1
                except:
                    result[2] = 1
                num = __sympy.S(f"{num} // 2")
            for i in range(3, 2 * num + 3, 2):
                if num == 1:
                    break
                while __sympy.S(f"{num} // {i}") == __sympy.S(f"{num} / {i}"):
                    try:
                        result[i] += 1
                    except:
                        result[i] = 1
                    num = __sympy.S(f"{num} // {i}")
            return result
        else:
            raise TypeError(f"unsupported type for prime factorization: int less than 2")
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
def LCM(num1: int, num2: int, sort: bool = False) -> int:
    '''
    一个求最小公倍数的函数

    通过两数乘积除以最大公因数进行计算

    参数:
        num1: 第一个正整数
        num2: 第二个正整数
        sort: 默认为 False ，如果 sort 参数为 True ，则默认 num1 为较大数字，num2 为较小数字
    '''
    if type(num1) == int and num1 > 0 and type(num2) == int and num2 > 0:
        return num1 * num2 // GCF(num1, num2, sort=sort)
    else:
        __operation_error(num1, num2, 'LCM')


# 快速排序
def quickly(data: list, parameter: any = None) -> list:
    '''
    列表的快速排序函数

    我都不用系列

    参数:
        data: 要排序的列表
        parameter: 默认为 None ，代表参数，为 None 时默认没有参数
    '''
    if parameter == None:
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
def calculator(input_text: str) -> int | float:
    text = list(input_text)
    finally_ = ''
    for i in range(len(text)):
        if input_text[i] == '^':
            text[i] = '**'
    for i in text:
        finally_ += i
    return eval(finally_)
'''


# 斐波那契数列
def fibonacci_sequence(index: int) -> int:
    return int(__sympy.S(f"1 / (5 ** 0.5) * (((1 + 5 ** 0.5) / 2) ** {index} - ((1 - 5 ** 0.5) / 2) ** {index})"))


# 质数判断
def prime(num: int) -> bool:
    if num > 1:
        prime = True
        for i in range(2, int(__sympy.S(f"{num} ** (1 / 2)") + 1)):
            if num % i == 0:
                prime = False
        return prime
    else:
        return False
