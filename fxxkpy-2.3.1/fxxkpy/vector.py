# coding:utf-8
# 坐标方法及方法类
class vector(object):
    # 两坐标距离
    @staticmethod
    def distance3(vector3: "Vector3", other_vector3: "Vector3") -> int | float:
        import sympy as __sympy
        res = __sympy.S(f"(({vector3.x} - {other_vector3.x}) ** 2 + ({vector3.y} - {other_vector3.y}) ** 2 + ({vector3.z} - {other_vector3.z}) ** 2) ** 0.5")
        if res == int(res):
            return int(res)
        else:
            return float(res)


# 三维坐标
class Vector3(object):
    def __init__(self: "Vector3", x: int | float, y: int | float, z: int | float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self: "Vector3", other: "Vector3") -> "Vector3":
        if type(other) == self.__class__:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception("TypeError: unsupported operand type(s) for +: 'Vector' and " + str_)

    def __radd__(self: "Vector3", other: "Vector3") -> "Vector3":
        if type(other) == self.__class__:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception("TypeError: unsupported operand type(s) for +: 'Vector' and " + str_)

    def __iadd__(self: "Vector3", other: "Vector3") -> "Vector3":
        if type(other) == self.__class__:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception("TypeError: unsupported operand type(s) for +: 'Vector' and " + str_)

    def __mul__(self: "Vector3", other: int) -> "Vector3":
        if type(other) == int:
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception("TypeError: unsupported operand type(s) for *: 'Vector' and " + str_)

    def __rmul__(self: "Vector3", other: int) -> "Vector3":
        if type(other) == int:
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception("TypeError: unsupported operand type(s) for *: 'Vector' and " + str_)

    def __imul__(self: "Vector3", other: int) -> "Vector3":
        if type(other) == int:
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            str_ = ''
            other_class = list(str(other.__class__))
            del other_class[-1]
            for index, item in enumerate(other_class):
                if index > 5:
                    str_ += item
            raise Exception("TypeError: unsupported operand type(s) for *: 'Vector' and " + str_)

    def __eq__(self: "Vector3", other: any) -> bool:
        if type(other) == self.__class__:
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

    def __ne__(self: "Vector3", other: any) -> bool:
        return not self.__eq__(other)

    def __str__(self: "Vector3") -> str:
        return f"{self.__dict__}"
