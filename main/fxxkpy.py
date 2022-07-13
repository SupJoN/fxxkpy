# coding:utf-8
import sympy


def Print():
    FxxkPy = '''\
.------..------..------..------..------..------.
|F.--. ||X.--. ||X.--. ||K.--. ||P.--. ||Y.--. |
| :(): || :/\: || :/\: || :/\: || :/\: || (\/) |
| ()() || (__) || (__) || :\/: || (__) || :\/: |
| '--'F|| '--'X|| '--'X|| '--'K|| '--'P|| '--'Y|
`------'`------'`------'`------'`------'`------'
'''
    print(FxxkPy)


class _Main(object):
    # 初始化方法
    def __init__(self, version):
        self.version = version
        self._cpp = _Cpp()
        self._c = _C()

    # 测试方法
    def _test(self):
        print(self.version + '  一切正常')

    # 快速排序
    def _quickly(self, data: list) -> list:
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
            return self._quickly(left) + [standard] + self._quickly(right)
        else:
            return original

    # 带参数的快速排序
    def _pquickly(self, data: list, parameter: int) -> list:
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
            return self._pquickly(left) + [standard] + self._pquickly(right)
        else:
            return original

    # 计算器
    def _calculator(self, input_text: str) -> int:
        text = list(input_text)
        finally_ = ''
        for i in range(len(text)):
            if input_text[i] == '^':
                text[i] = '**'
        for i in text:
            finally_ += i
        return eval(finally_)

    # 斐波那契数列
    def _fibonacci_sequence(self, index: int) -> int:
        return int(sympy.S('1 / (5 ** 0.5) * (((1 + 5 ** 0.5) / 2) ** ' + str(index) + ' - ((1 - 5 ** 0.5) / 2) ** ' + str(index) + ')'))

    # 质数判断
    def _prime(self, num: int) -> bool:
        if num > 1:
            prime = True
            for i in range(2, int(sympy.S(str(num) + ' ** (1 / 2)') + 1)):
                if num % i == 0:
                    prime = False
            return prime
        else:
            return False


# c++类
class _Cpp():
    def __init__(self):
        self.cout = _Cout()
        self.endl = '\n'


# cout类
class _Cout():
    def __init__(self):
        pass

    # << 方法
    def __lshift__(self, other: str):
        print(other, end = '')
        return self


# c类
class _C():
    def __init__(self):
        self.printf = print


Print()


_main = _Main('v0.2.6-beta')
cpp = _main._cpp
c = _main._c
test = _main._test
quickly = _main._quickly
pquickly = _main._pquickly
calculator = _main._calculator
fibonacci_sequence = _main._fibonacci_sequence
prime = _main._prime
