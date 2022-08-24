# coding:utf-8
# c类
class C():
    # printf方法
    def printf(content) -> None:
        print(content, end='')


# c++类
# cout类
class _Cout():
    # << 方法
    def __lshift__(self, other: str) -> "_Cout":
        print(other, end='')
        return self


class Cpp():
    cout = _Cout()
    endl = '\n'


# Java类
class Java():
    class System():
        class out():
            println = print
