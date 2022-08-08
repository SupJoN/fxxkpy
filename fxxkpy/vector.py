# -*- coding: UTF-8 -*-
import sympy as __sympy


# 两坐标距离
def _distance3(vector3: "Vector3", other_vector3: "Vector3"):
    res = __sympy.S('((' + str(vector3.x) + ' - ' + str(other_vector3.x) + ') ** 2 + \
                    (' + str(vector3.y) + ' - ' + str(other_vector3.y) + ') ** 2 + \
                    (' + str(vector3.z) + ' - ' + str(other_vector3.z) + ') ** 2) ** 0.5')
    if res == int(res):
        return int(res)
    else:
        return float(res)


# 坐标方法及方法类
class vector():
    distance3 = _distance3


# 三维坐标
class Vector3():
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Vector3") -> "Vector3":
        if type(other) == self.__class__:
            return Vector3(self.x + other.x,
                           self.y + other.y,
                           self.z + other.z)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception(
                "TypeError: unsupported operand type(s) for +: 'Vector' and " + str_)

    def __radd__(self, other: "Vector3") -> "Vector3":
        if type(other) == self.__class__:
            return Vector3(self.x + other.x,
                           self.y + other.y,
                           self.z + other.z)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception(
                "TypeError: unsupported operand type(s) for +: 'Vector' and " + str_)

    def __iadd__(self, other: "Vector3") -> "Vector3":
        if type(other) == self.__class__:
            return Vector3(self.x + other.x,
                           self.y + other.y,
                           self.z + other.z)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception(
                "TypeError: unsupported operand type(s) for +: 'Vector' and " + str_)

    def __mul__(self, other: int) -> "Vector3":
        if type(other) == int:
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception(
                "TypeError: unsupported operand type(s) for *: 'Vector' and " + str_)

    def __rmul__(self, other: int) -> "Vector3":
        if type(other) == int:
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception(
                "TypeError: unsupported operand type(s) for *: 'Vector' and " + str_)

    def __imul__(self, other: int) -> "Vector3":
        if type(other) == int:
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception(
                "TypeError: unsupported operand type(s) for *: 'Vector' and " + str_)

    def __eq__(self, other: "Vector3") -> bool:
        if type(other) == self.__class__:
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

    def __ne__(self, other: "Vector3") -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"{self.__dict__}"
