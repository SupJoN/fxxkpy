# coding:utf-8
class Enigma(object):
    '''
    恩格玛机
    '''
    def __init__(self, data: list[dict]) -> None:
        class Rotor(object):
            """
            转子
            """
            def __init__(self, PasswordTable: dict[int, int], RotationNumber: int, LAST: "Rotor" | None) -> None:
                self.PT: dict[int, int] = PasswordTable
                self.RotationNumber: int = RotationNumber
                self.LAST: "Rotor" | None = LAST
                self.NEXT: "Rotor" | "Reflector" | None = None
                self.direction: bool = True
                self.length: int = len(self.PT)
                self.direction: int = 0
                self.location: int = 0

            def move(self) -> None:
                self.location += self.RotationNumber
                self.direction = (self.direction + 1) % 2
                if self.location > self.length:
                    self.location %= self.length
                    if self.direction:
                        if self.NEXT is not None:
                            self.NEXT.move()
                    else:
                        if self.LAST is not None:
                            self.LAST.move()

            def change(self, index: int) -> int:
                return self.PT[(index + self.location) % self.length]

        class Reflector(object):
            """反射板"""
            def __init__(self, PasswordTable: dict[int, int], LAST: "Rotor" | None) -> None:
                self.PT: dict[int, int] = PasswordTable
                self.LAST: "Rotor" | None = LAST

            def move(self) -> None:
                self.LAST.move()

            def change(self, index: int) -> int:
                return self.PT[index]

        self.rotor: list[Rotor | Reflector] = []
        for index, item in enumerate(data):
            if item["type"] == "Rotor":
                PasswordTable = item["PasswordTable"]
                RotationNumber = item["RotationNumber"]
                try:
                    LAST = self.rotor[index - 1]
                except:
                    LAST = None
                self.rotor.append(Rotor(PasswordTable, RotationNumber, LAST))
            if item["type"] == "Reflector":
                PasswordTable = item["PasswordTable"]
                try:
                    LAST = self.rotor[index - 1]
                except:
                    LAST = None
                self.rotor.append(Reflector(PasswordTable, LAST))
        for index, item in enumerate(self.rotor):
            if index != len(self.rotor) - 1:
                item.NEXT = self.rotor[index + 1]

    def change(self, index: int):
        result = index
        for i in self.rotor:
            result = i.change(result)
        self.rotor[-1].move()
        return result
