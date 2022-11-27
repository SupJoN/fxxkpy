# coding:utf-8
class ThreeDimensions(object):
    class Coordinate(object):
        try:
            import sympy
            sympy_: bool = True
            del sympy
        except:
            sympy_: bool = False

        def __init__(self, x: float, y: float, z: float) -> None:
            self.x: float = x
            self.y: float = y
            self.z: float = z

        def __repr__(self) -> str:
            return str((self.x, self.y, self.z))

        def __str__(self) -> str:
            return self.__repr__()

        @staticmethod
        def distance(coordinate: "ThreeDimensions.Coordinate", other_coordinate: "ThreeDimensions.Coordinate") -> float:
            if ThreeDimensions.Coordinate.sympy_:
                import sympy
                return float(sympy.S(f"(({coordinate.x} - {other_coordinate.x}) ** 2 + ({coordinate.y} - {other_coordinate.y}) ** 2 + ({coordinate.z} - {other_coordinate.z}) ** 2) ** 0.5"))
            else:
                return ((coordinate.x - other_coordinate.x) ** 2 + (coordinate.y - other_coordinate.y) ** 2 + (coordinate.z - other_coordinate.z) ** 2) ** 0.5

    class Model(object):
        ...

    class VirtualObject(object):
        from typing import Any as __Any
        from typing import overload as __overload

        @__overload
        def __init__(self, model: "ThreeDimensions.Model", coordinate: "ThreeDimensions.Coordinate") -> None:
            ...

        @__overload
        def __init__(self, model: "ThreeDimensions.Model", x: float, y: float, z: float) -> None:
            ...

        def __init__(self, *args: __Any) -> None:
            if len(args) == 2:
                if isinstance(args[0], ThreeDimensions.Model):
                    self.__model: ThreeDimensions.Model = args[0]
                else:
                    import re
                    function: str = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function: str = function[14:len(function) - 4]
                    model: str = str(ThreeDimensions.Model)
                    str_model: str = model[8:len(model) - 2]
                    raise TypeError(f"{function}() require the third arguments to be {str_model}, but it is not {str_model}")
                if isinstance(args[1], ThreeDimensions.Coordinate):
                    self.__coordinate: ThreeDimensions.Coordinate = args[1]
                else:
                    import re
                    function: str = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function: str = function[14:len(function) - 4]
                    coordinate: str = str(ThreeDimensions.Coordinate)
                    str_coordinate: str = coordinate[8:len(coordinate) - 2]
                    raise TypeError(f"{function}() require the third arguments to be {str_coordinate}, but it is not {str_coordinate}")
            elif len(args) == 4:
                if isinstance(args[0], ThreeDimensions.Model):
                    self.__model: ThreeDimensions.Model = args[0]
                else:
                    import re
                    function: str = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function: str = function[14:len(function) - 4]
                    model: str = str(ThreeDimensions.Model)
                    str_model: str = model[8:len(model) - 2]
                    raise TypeError(f"{function}() require the third arguments to be {str_model}, but it is not {str_model}")
                if isinstance(args[1], float) and isinstance(args[2], float) and isinstance(args[3], float):
                    self.__coordinate: ThreeDimensions.Coordinate = ThreeDimensions.Coordinate(float(args[1]), float(args[2]), float(args[3]))
                else:
                    import re
                    function: str = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function: str = function[14:len(function) - 4]
                    raise TypeError(f"{function}() require the third, fourth, and fifth arguments to be int or float, but they are not all int or float")
            else:
                import re
                function: str = re.match("<bound method \S* of", repr(self.__init__)).group()
                function: str = function[14:len(function) - 4]
                raise TypeError(f"{function}() takes 2 or 4 positional argument but {len(args) + 1} were given")

        @property
        def model(self) -> "ThreeDimensions.Model":
            return self.__model

        @property
        def coordinate(self) -> "ThreeDimensions.Coordinate":
            return self.__coordinate

        del __Any, __overload
