# coding:utf-8
import sympy


def __Print() -> None:
    FxxkPy = '''
.------..------..------..------..------..------.
|F.--. ||X.--. ||X.--. ||K.--. ||P.--. ||Y.--. |
| :(): || :/\: || :/\: || :/\: || :/\: || (\/) |
| ()() || (__) || (__) || :\/: || (__) || :\/: |
| '--'F|| '--'X|| '--'X|| '--'K|| '--'P|| '--'Y|
`------'`------'`------'`------'`------'`------'
'''
    print(FxxkPy)


# 快速排序
def quickly(data: list) -> list:
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


# 带参数的快速排序
def pquickly(data: list, parameter: int) -> list:
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
        return pquickly(left) + [standard] + pquickly(right)
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


__Print()

