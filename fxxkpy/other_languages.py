# coding:utf-8
# c类
class C():
    # printf方法
    def printf(content):
        print(content, end='')


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


# Java类
class _out():
    println = print


class _System():
    out = _out()


class Java():
    System = _System
