# coding:utf-8
def Print():
    FxxkPy = r'''
.------..------..------..------..------..------.
|F.--. ||X.--. ||X.--. ||K.--. ||P.--. ||Y.--. |
| :(): || :/\: || :/\: || :/\: || :/\: || (\/) |
| ()() || (__) || (__) || :\/: || (__) || :\/: |
| '--'F|| '--'X|| '--'X|| '--'K|| '--'P|| '--'Y|
`------'`------'`------'`------'`------'`------'
'''
    print(FxxkPy)

class _Main(object):
    def __init__(self):
        pass

    def _test(self):
        print('一切正常')

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


Print()


_main = _Main()
test = _main.test
quickly = _main._quickly
