# coding:utf-8
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
    def _calculator(self, input_text: str):
        text = list(input_text)
        finally_ = ''
        for i in range(len(text)):
            if input_text[i] == '^':
                text[i] = '**'
        for i in text:
            finally_ += i
        return eval(finally_)

Print()


_main = _Main('v0.2.4-beta')
test = _main._test
quickly = _main._quickly
pquickly = _main._pquickly
calculator = _main._calculator
