# coding:utf-8
# cout类
class _Cout():
    def __init__(self) -> None:
        pass

    # << 方法
    def __lshift__(self, other: str) -> "_Cout":
        print(other, end='')
        return self


# c++类
class Cpp():
    cout = _Cout()
    endl = '\n'
