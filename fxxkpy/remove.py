# coding:utf-8
def warning_remove(file: str, isself: bool = False) -> None:
    '''
    传入要删的文件的绝对路径
    '''
    import os
    from colorama import Fore, Style

    if os.path.exists(file):
        confirm: str = input(f"{Fore.YELLOW}警告{Style.RESET_ALL}: {'此文件' if isself else file} 将被删除(y/N)")
        try:
            if confirm == "y" or confirm == "Y":
                executing: bool = True
            else:
                executing: bool = False
        except Exception:
            executing: bool = False
        if executing:
            os.remove(file)
    else:
        raise FileNotFoundError(f"系统找不到指定的文件: {file}")
