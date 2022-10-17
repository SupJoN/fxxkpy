# coding:utf-8
def __start() -> None:
    FxxkPy: str = '''\
.------..------..------..------..------..------.
|F.--. ||X.--. ||X.--. ||K.--. ||P.--. ||Y.--. |
| :(): || :/\: || :/\: || :/\: || :/\: || (\/) |
| ()() || (__) || (__) || :\/: || (__) || :\/: |
| '--'F|| '--'X|| '--'X|| '--'K|| '--'P|| '--'Y|
`------'`------'`------'`------'`------'`------'\
'''
    from random import randint
    from sys import version_info

    from colorama import Fore, Style

    from .version import ver

    color: str = '' if not randint(0, 2) else Fore.GREEN if not randint(0, 4) else Fore.YELLOW if randint(0, 1) else Fore.BLUE
    print(f"{color}FxxkPy {ver} (Python {'.'.join(map(str, version_info[0:3]))})")
    print(FxxkPy, end='')
    print(Style.RESET_ALL)

    del randint, version_info, Fore, Style, ver, color


__start()
