# coding:utf-8
import sympy


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
    return int(sympy.S('1 / (5 ** 0.5) * (((1 + 5 ** 0.5) / 2) ** ' + str(index) + ' - ((1 - 5 ** 0.5) / 2) ** ' + str(index) + ')'))


# 质数判断
def prime(num: int) -> bool:
    if num > 1:
        prime = True
        for i in range(2, int(sympy.S(str(num) + ' ** (1 / 2)') + 1)):
            if num % i == 0:
                prime = False
        return prime
    else:
        return False
