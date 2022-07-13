# coding:utf-8
# 快速排序
def quickly(data: list) -> list:
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
        return quickly(left) + [standard] + quickly(right)
    else:
        return original


# 带参数的快速排序
def pquickly(data: list, parameter: int) -> list:
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
        return pquickly(left) + [standard] + pquickly(right)
    else:
        return original
