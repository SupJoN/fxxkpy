# coding:utf-8
import typing as _typing
import io as _io


def safe_eq(a: str, b: str) -> bool:
    '''
    超级安全的字符串比较

    在密码比较上, a 应该为用户的输入, b 为保存的密码
    '''
    length: int = len(b)
    ne: bool = False
    for index, item in enumerate(a):
        if item != b[index % length]:
            ne: bool = True
    return not ne and length - 1 == index


def clear_string(content: str) -> str:
    '''
    清洁字符串

    去除无用的转义字符
    '''
    if isinstance(content, str):
        from .FullBaseObject import FullDict

        result: str = ""
        line: FullDict = FullDict(" ", clear=True)
        index: int = 0
        max_index: int = 0
        for i in content:
            if i == "\n":
                print(f"{max_index=}", line)
                result += "".join((line[i] for i in range(max_index + 1))) + "\n"
                index: int = 0
                max_index: int = 0
                line.clear()
            elif i == "\b":
                index -= 1
            elif i == "\t":
                index: int = index + 8 - index % 8
            elif i == "\r":
                index: int = 0
            else:
                max_index: int = max(index, max_index)
                line[index]: str = i
                index += 1
        result += "".join((line[i] for i in range(max_index)))
        return result
    else:
        raise TypeError("clear_string's parameter must be a str")


def pyin(prompt: str = "", quantity: int = 1, inType: type = float, mustReturnTuple: bool = False) -> (int | float | complex | str | tuple[int | float | complex | str]):
    '''
    仿 scanf 的输入方法

    提供了 `int` `float` `complex` `str` 的输入模式

    参数:
        prompt: 提示语, 默认为 `""`
        quantity: 输入的个数, 默认为 `1`
        inType: 输入的类型, 默认为 `float`
        mustReturnTuple: 返回值是否必须为 `tuple`, 默认为 `False`
    '''
    if isinstance(quantity, int) and quantity > 0:
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
                            except Exception:
                                pass
            elif inType == complex:
                for i in inlist:
                    result: list = re.findall(rule, i)
                    for j in inlist:
                        if j == i:
                            try:
                                values.append(eval(f"1{i}" if (i := i.replace("i", "j").replace("+j", "+1j").replace("-j", "-1j"))[0] == "j" else i))
                            except Exception:
                                pass
        if mustReturnTuple or quantity - 1:
            return tuple(values[0:quantity])
        else:
            return values[0]
    else:
        raise TypeError("pyin() needs the \'quantity\' who is 'int' and more than zero")


def pyout(*args: _typing.Any, **kwargs: _typing.Any) -> None:
    '''
    仿 printf 的输出方法
    '''
    print(str(args[0]) % args[1::], **kwargs)


def tprint(*args: _typing.Any, t: _typing.Iterator[int] | int, sep: str = " ", end="\n", file: _io.TextIOWrapper | None = None, flush: bool = False) -> None:
    '''
    `\\t` 输出

    参数:
        `*args`: 要输出的对象
        `t`: 类型为 int 时, `\\r` 后固定 `t` 个 `\\t`; 类型为 Iterator 时, `\\r` 后为 `t` 中对应的个数
        `sep`: 在值之间插入字符串, 默认为空格
        `end`: 在最后一个值之后追加的字符串, 默认为换行符
    '''
    from collections.abc import Iterable
    t_now: int = 0
    print(f"{''.join((f'{item}{sep}{chr(13)}{chr(9) * (t_now := 0 if chr(10) == str(item)[-1] else (0 if chr(10) in str(item) else t_now) + (t if not isinstance(t, Iterable) else t[index] if len(t) > index else 0))}' for index, item in enumerate(args[:-1:])))}{args[-1]}" if len(args) else "", end=end, file=file, flush=flush)


def titerprint(args: _typing.Iterator[_typing.Iterator[_typing.Any]], t: _typing.Iterator[int] | int, sep: str = " ", end="\n", file: _io.TextIOWrapper | None = None, flush: bool = False) -> None:
    '''
    `\\t` `Iterator` 输出

    参数:
        `args`: 要输出的可迭代对象
        `t`: 类型为 int 时, `\\r` 后固定 `t` 个 `\\t`; 类型为 Iterator 时, `\\r` 后为 `t` 中对应的个数
        `sep`: 在值之间插入字符串, 默认为空格
        `end`: 在最后一个值之后追加的字符串, 默认为换行符
    '''
    iterlist = []
    for i in args:
        iterlist.extend(i)
    tprint(*iterlist, t=t, sep=sep, end=end, file=file, flush=flush)


def getpass(username_prompt: str = "username", password_prompt: str = "password") -> tuple[str, str]:
    '''
    获取用户名及密码
    '''
    from getpass import getpass
    user: str = input(f"{username_prompt}: ")
    password: str = getpass(f"{password_prompt}: ")
    return user, password


del _typing
del _io
