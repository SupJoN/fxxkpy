# coding:utf-8
def pyin(prompt: str = "", quantity: int = 1, inType: type = float, mustReturnTuple: bool = False) -> int | float | complex | str | tuple[int | float | complex | str]:
    '''
    仿 scanf 的输入方法

    提供了 ```int``` ```float``` ```complex``` ```str``` 的输入模式

    参数:
        prompt: 提示语, 默认为 ```""```
        quantity: 输入的个数, 默认为 ```1```
        inType: 输入的类型, 默认为 ```float```
        mustReturnTuple: 返回值是否必须为 ```tuple```, 默认为 ```False```
    '''
    if type(quantity) == int and quantity > 0:
        import re

        RULE: dict[type:str] = {
            int: "[\\+\\-]?\\d+",
            float: "[\\+\\-]?\\d*[\\.]?\\d*",
            complex: "[\\+\\-]?\\d*[\\.]?\\d*[\\+\\-]?\\d*[\\.]?\\d*[ij]?",
            str: "",
        }

        rule: str = RULE[inType]
        print(prompt, end="")
        values: list = []
        while len(values) < quantity:
            inlist: list[str] = input().split()
            if inType == str:
                values += inlist
            elif inType == int:
                for i in inlist:
                    result: list = re.findall(rule, i)
                    if result:
                        if result[0] == i:
                            values.append(eval(i))
            elif inType == float:
                for i in inlist:
                    result: list = re.findall(rule, i)
                    for j in inlist:
                        if j == i:
                            try:
                                values.append(eval(i))
                            except:
                                pass
            elif inType == complex:
                for i in inlist:
                    result: list = re.findall(rule, i)
                    for j in inlist:
                        if j == i:
                            try:
                                i: str = i.replace("i", "j")
                                i: str = i.replace("+j", "+1j")
                                i: str = i.replace("-j", "-1j")
                                i: str = f"1{i}" if i[0] == "j" else i
                                values.append(eval(i))
                            except:
                                pass
        if mustReturnTuple or quantity - 1:
            return tuple(values[0:quantity])
        else:
            return values[0]
    else:
        raise TypeError("pyin() needs the \'quantity\' who is 'int' and more than zero")


def pyout(*args: any, **kwargs: any) -> None:
    print(str(args[0]).format(*args[1::]), **kwargs)


def getpass(username_prompt="username", password_prompt="password"):
    from getpass import getpass

    user = input(f"{username_prompt}: ")
    password = getpass(f"{password_prompt}: ")

    return user, password
