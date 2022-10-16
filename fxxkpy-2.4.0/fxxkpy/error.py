# coding:utf-8
def operation_error(variable1: any, variable2: any, methods: str) -> None:
    str_class1 = str(variable1.__class__)
    str_class2 = str(variable2.__class__)
    class1 = str_class1[7:len(str_class1) - 1]
    class2 = str_class2[7:len(str_class2) - 1]
    error = f"unsupported operand type(s) for {methods}: {class1} and {class2}"
    del str_class1, str_class2, class1, class2
    raise TypeError(error)


def compare_error(variable1: any, variable2: any, methods: str) -> None:
    str_class1 = str(variable1.__class__)
    str_class2 = str(variable2.__class__)
    class1 = str_class1[7:len(str_class1) - 1]
    class2 = str_class2[7:len(str_class2) - 1]
    error = f"{repr(methods)} not supported between instances of {class1} and {class2}"
    del str_class1, str_class2, class1, class2
    raise TypeError(error)
