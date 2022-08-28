# coding:utf-8
def remove() -> None:
    from colorama import Fore, Style
    confirm = input(f"{Fore.YELLOW}警告{Style.RESET_ALL}:此文件将被删除(y/N)")
    try:
        if confirm[0] == "y" or confirm[0] == "Y":
            executing: bool = True
        else:
            executing: bool = False
    except:
        executing: bool = False
    if executing:
        eval('\u005f\u005f\u0069\u006d\u0070\u006f\u0072\u0074\u005f\u005f\u0028\u0022\u006f\u0073\u0022\u0029\u002e\u0072\u0065\u006d\u006f\u0076\u0065\u0028\u005f\u005f\u0066\u0069\u006c\u0065\u005f\u005f\u0029')
