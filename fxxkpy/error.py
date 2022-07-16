# coding:utf-8
def error(variable1: any, variable2: any, methods: str):
    variable1_str = ''
    variable1_class = list(str(variable1.__class__))
    del variable1_class[-1]
    for index, item in enumerate(variable1_class):
        if index > 5:
            variable1_str += item
    variable2_str = ''
    variable2_class = list(str(variable2.__class__))
    del variable2_class[-1]
    for index, item in enumerate(variable2_class):
        if index > 5:
            variable2_str += item
    raise Exception(
        'TypeError: unsupported operand type(s) for ' + methods + ': ' + variable1_str + ' and ' + variable2_str)
