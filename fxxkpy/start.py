# coding:utf-8
def __start() -> None:
    FxxkPy = '''\
.------..------..------..------..------..------.
|F.--. ||X.--. ||X.--. ||K.--. ||P.--. ||Y.--. |
| :(): || :/\: || :/\: || :/\: || :/\: || (\/) |
| ()() || (__) || (__) || :\/: || (__) || :\/: |
| '--'F|| '--'X|| '--'X|| '--'K|| '--'P|| '--'Y|
`------'`------'`------'`------'`------'`------'\
'''
    from random import randint as rint
    from sys import version_info as info
    from colorama import Fore, Style
    from .version import ver
    color = '' if rint(0, 1) else Fore.YELLOW if rint(0, 1) else Fore.BLUE
    print(f"{color}fxxkpy {ver} (Python {'.'.join(map(str, info[0:3]))})")
    print(FxxkPy, end='')
    print(Style.RESET_ALL)
    del rint, info, Fore, Style, ver, color


__start()
