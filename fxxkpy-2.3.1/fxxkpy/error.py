# coding:utf-8
def operation_error(variable1: any, variable2: any, methods: str) -> None:
    class1 = str(variable1.__class__)[7:len(str(variable1.__class__)) - 1]
    class2 = str(variable2.__class__)[7:len(str(variable2.__class__)) - 1]
    raise TypeError(f"unsupported operand type(s) for {methods}: {class1} and {class2}")
