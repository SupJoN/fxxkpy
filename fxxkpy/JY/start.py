# coding:utf-8
def __start() -> None:
    JY: str = '''\
.------..------.
|J.--. ||Y.--. |
| :(): || (\/) |
| ()() || :\/: |
| '--'J|| '--'Y|
`------'`------'\
'''
    I_LIKE_JY: str = '''\
.------.     .------..------..------..------.     .------..------.
|I.--. |.-.  |L.--. ||I.--. ||K.--. ||E.--. |.-.  |J.--. ||Y.--. |
| (\/) ((5)) | :/\: || (\/) || :/\: || (\/) ((5)) | :(): || (\/) |
| :\/: |'-.-.| (__) || :\/: || :\/: || :\/: |'-.-.| ()() || :\/: |
| '--'I| ((1)) '--'L|| '--'I|| '--'K|| '--'E| ((1)) '--'J|| '--'Y|
`------'  '-'`------'`------'`------'`------'  '-'`------'`------'
'''
    from random import randint
    from sys import version_info

    from colorama import Fore, Style

    from .version import ver
    from ..version import ver as fxxkpy_ver

    content: str = JY if randint(1, 97) - 1 else I_LIKE_JY
    color: str = "" if not randint(0, 2) else Fore.GREEN if not randint(0, 4) else Fore.YELLOW if randint(0, 1) else Fore.BLUE
    print(f"{color}JY {ver} (FxxkPy {fxxkpy_ver})")
    print(content, end="")
    print(Style.RESET_ALL)

    del randint, version_info, Fore, Style, ver, color


__start()
