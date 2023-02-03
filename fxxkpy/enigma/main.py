# coding:utf-8
class Enigma(object):
    '''
    恩格玛机

    例子
    ```
    Enigma([{"type": "Rotor", "PasswordTable": {1, 2}, "RotationNumber": 2}, {"type": "Rotor", "PasswordTable": {2, 1}, "RotationNumber": 2}])
    ```
    '''
    def __init__(self, data: list[dict]) -> None:
        class Rotor(object):
            """
            转子
            """
            def __init__(self, PasswordTable: dict[int, int], RotationNumber: int, LAST: "Rotor" = None) -> None:
                self.PT: dict[int, int] = PasswordTable
                self.RotationNumber: int = RotationNumber
                self.LAST: "Rotor" = LAST
                self.NEXT: "Rotor" | "Reflector" = None
                self.direction: bool = True
                self.length: int = len(self.PT)
                self.direction: int = 0
                self.location: int = 0

            def move(self) -> None:
                self.location += self.RotationNumber
                self.direction: bool = (self.direction + 1) % 2
                if self.location > self.length:
                    self.location %= self.length
                    if self.direction:
                        if self.NEXT != None:
                            self.NEXT.move()
                    else:
                        if self.LAST != None:
                            self.LAST.move()

            def change(self, index: int) -> int:
                return self.PT[(index + self.location) % self.length]

        class Reflector(object):
            """反射板"""
            def __init__(self, PasswordTable: dict[int, int], LAST: "Rotor") -> None:
                self.PT: dict[int, int] = PasswordTable
                self.LAST: "Rotor" = LAST

            def move(self) -> None:
                self.LAST.move()

            def change(self, index: int) -> int:
                return self.PT[index]

        self.rotor: list[Rotor | Reflector] = []
        for index, item in enumerate(data):
            if item["type"] == "Rotor":
                PasswordTable: str = item["PasswordTable"]
                RotationNumber: str = item["RotationNumber"]
                try:
                    LAST: Rotor = self.rotor[index - 1]
                except Exception:
                    LAST: None = None
                self.rotor.append(Rotor(PasswordTable, RotationNumber, LAST))
            if item["type"] == "Reflector":
                PasswordTable = item["PasswordTable"]
                try:
                    LAST: Reflector = self.rotor[index - 1]
                except Exception:
                    LAST: None = None
                self.rotor.append(Reflector(PasswordTable, LAST))
        for index, item in enumerate(self.rotor):
            if index != len(self.rotor) - 1:
                item.NEXT: Rotor = self.rotor[index + 1]

    def change(self, index: int) -> int:
        result: int = index
        for i in self.rotor:
            result: int = i.change(result)
        self.rotor[-1].move()
        return result
