# coding:utf-8
# 坐标方法及方法类
class vector(object):
    # 两坐标距离
    @staticmethod
    def distance3(vector3: "Vector3", other_vector3: "Vector3") -> float:
        from sympy import S

        res = S(f"(({vector3.x} - {other_vector3.x}) ** 2 + ({vector3.y} - {other_vector3.y}) ** 2 + ({vector3.z} - {other_vector3.z}) ** 2) ** 0.5")
        return float(res)


# 三维坐标
class Vector3(object):
    from typing import Any as __Any

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __add__(self, other: "Vector3") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            from .error import operation_error
            operation_error(self, other, "+")

    def __radd__(self, other: "Vector3") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            from .error import operation_error
            operation_error(other, self, "+")

    def __iadd__(self, other: "Vector3") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            from .error import operation_error
            operation_error(self, other, "+=")

    def __mul__(self, other: int) -> "Vector3":
        if isinstance(other, int):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            from .error import operation_error
            operation_error(self, other, "*")

    def __rmul__(self, other: int) -> "Vector3":
        if isinstance(other, int):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            from .error import operation_error
            operation_error(other, self, "*")

    def __imul__(self, other: int) -> "Vector3":
        if isinstance(other, int):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            from .error import operation_error
            operation_error(self, other, "*=")

    def __eq__(self, other: __Any) -> bool:
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

    def __ne__(self, other: __Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"{self.__dict__}"

    del __Any
