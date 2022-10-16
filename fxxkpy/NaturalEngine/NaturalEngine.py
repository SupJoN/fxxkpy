# coding:utf-8
class ThreeDimensions(object):
    class Coordinate(object):
        def __init__(self, x: float, y: float, z: float) -> None:
            self.x = x
            self.y = y
            self.z = z

        def __repr__(self) -> str:
            return str((self.x, self.y, self.z))

        def __str__(self) -> str:
            return self.__repr__()

        @staticmethod
        def distance(coordinate: "ThreeDimensions.Coordinate", other_coordinate: "ThreeDimensions.Coordinate") -> float:
            import sympy as __sympy
            res = __sympy.S(f"(({coordinate.x} - {other_coordinate.x}) ** 2 + ({coordinate.y} - {other_coordinate.y}) ** 2 + ({coordinate.z} - {other_coordinate.z}) ** 2) ** 0.5")
            return float(res)

    class Model(object):
        ...

    class VirtualObject(object):
        from typing import overload as __overload

        @__overload
        def __init__(self, model, coordinate: "ThreeDimensions.Coordinate") -> None:
            ...

        @__overload
        def __init__(self, x: float, y: float, z: float) -> None:
            ...

        def __init__(self, *args: any) -> None:
            if len(args) == 2:
                if type(args[1]) == ThreeDimensions.Model:
                    self.__model = args[0]
                else:
                    import re
                    function = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function = function[14:len(function) - 4]
                    model = str(ThreeDimensions.Model)
                    str_model = model[8:len(model) - 2]
                    raise TypeError(f"{function}() require the third arguments to be {str_model}, but it is not {str_model}")
                if type(args[1]) == ThreeDimensions.Coordinate:
                    self.__coordinate = args[1]
                else:
                    import re
                    function = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function = function[14:len(function) - 4]
                    coordinate = str(ThreeDimensions.Coordinate)
                    str_coordinate = coordinate[8:len(coordinate) - 2]
                    raise TypeError(f"{function}() require the third arguments to be {str_coordinate}, but it is not {str_coordinate}")
            elif len(args) == 4:
                if type(args[1]) == ThreeDimensions.Model:
                    self.__model = args[0]
                else:
                    import re
                    function = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function = function[14:len(function) - 4]
                    model = str(ThreeDimensions.Model)
                    str_model = model[8:len(model) - 2]
                    raise TypeError(f"{function}() require the third arguments to be {str_model}, but it is not {str_model}")
                if type(args[1]) == float or int and type(args[2]) == float or int and type(args[3]) == float or int:
                    for i in range(1, 4):
                        args[i] = float(args[i])
                    self.__coordinate = ThreeDimensions.Coordinate(args[1], args[2], args[3])
                else:
                    import re
                    function = re.match("<bound method \\S+ of", repr(self.__init__)).group()
                    function = function[14:len(function) - 4]
                    raise TypeError(f"{function}() require the third, fourth, and fifth arguments to be int or float, but they are not all int or float")
            else:
                import re
                function = re.match("<bound method \S* of", repr(self.__init__)).group()
                function = function[14:len(function) - 4]
                raise TypeError(f"{function}() takes 2 or 4 positional argument but {len(args) + 1} were given")

        @property
        def model(self) -> "ThreeDimensions.Model":
            return self.__model

        @property
        def coordinate(self) -> "ThreeDimensions.Coordinate":
            return self.__coordinate
