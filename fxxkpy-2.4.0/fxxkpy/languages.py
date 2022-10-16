# coding:utf-8
# c类
class c(object):
    # printf方法
    def printf(content) -> None:
        print(content, end='')


# c++类
class cpp(object):
    # cout类
    class __Cout(object):
        # << 方法
        def __lshift__(self, other: str) -> "cpp.__Cout":
            print(other, end='')
            return self

    cout = __Cout()
    endl = '\n'


# Java类
class java(object):
    class System():
        class out():
            println = print
